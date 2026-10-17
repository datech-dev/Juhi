import uuid
from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.authorization import get_current_active_user
from app.domain.models.billing import CreditAccount, CreditLedgerEntry
from app.domain.models.companion import CompanionProfile
from app.domain.models.conversation import Conversation, ConversationSummary, Message
from app.domain.models.media import CreditReservation, GenerationJob, MediaAsset
from app.domain.models.memory import MemoryItem
from app.domain.models.user import ConsentRecord, ExternalIdentity, User, UserPreference
from app.infrastructure.database.session import get_db
from app.schemas.user import UserConsentRequest, UserDataExportResponse

router = APIRouter(prefix="/users", tags=["User Privacy & Account"])


@router.post("/me/consent")
async def record_user_consent(
    consent_data: UserConsentRequest,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Records an explicit consent event (e.g. AI disclosure, 18+ age verification, memory consent).
    Also updates user's age_assurance_status if purpose is age verification.
    """
    record = ConsentRecord(
        id=uuid.uuid4(),
        user_id=user.id,
        purpose=consent_data.purpose,
        decision=consent_data.decision,
        notice_version=consent_data.notice_version,
        capture_channel="mobile_app",
        metadata_json=consent_data.metadata_json,
    )
    db.add(record)

    if consent_data.purpose == "age_verification_18_plus" and consent_data.decision == "granted":
        user.age_assurance_status = "verified_adult"

    # Mark onboarding completed in preferences if AI disclosure and age verified
    pref_stmt = select(UserPreference).where(UserPreference.user_id == user.id)
    pref_res = await db.execute(pref_stmt)
    prefs = pref_res.scalar_one_or_none()
    if prefs:
        settings = dict(prefs.settings_json or {})
        settings[f"consent_{consent_data.purpose}"] = consent_data.decision
        if consent_data.purpose in ("ai_companion_disclosure", "age_verification_18_plus"):
            settings["onboarding_completed"] = True
        prefs.settings_json = settings

    await db.commit()
    return {
        "status": "success",
        "purpose": consent_data.purpose,
        "decision": consent_data.decision,
    }


@router.get("/me/export", response_model=UserDataExportResponse)
async def export_user_data(
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Exports all user data in a portable JSON format adhering to PRD MEM-11 and GDPR/DPDP requirements.
    """
    # 1. User and preferences
    pref_stmt = select(UserPreference).where(UserPreference.user_id == user.id)
    prefs = (await db.execute(pref_stmt)).scalar_one_or_none()
    pref_data = {
        "ui_language": prefs.ui_language,
        "preferred_reply_language": prefs.preferred_reply_language,
        "code_switching_enabled": prefs.code_switching_enabled,
        "timezone": prefs.timezone,
        "theme_mode": prefs.theme_mode,
        "memory_enabled": prefs.memory_enabled,
        "settings_json": prefs.settings_json,
    } if prefs else None

    # 2. Consent records
    consent_stmt = select(ConsentRecord).where(ConsentRecord.user_id == user.id)
    consent_records = (await db.execute(consent_stmt)).scalars().all()
    consent_data = [
        {
            "purpose": c.purpose,
            "decision": c.decision,
            "notice_version": c.notice_version,
            "created_at": c.created_at.isoformat() if c.created_at else None,
        }
        for c in consent_records
    ]

    # 3. Companions
    comp_stmt = select(CompanionProfile).where(CompanionProfile.user_id == user.id)
    companions = (await db.execute(comp_stmt)).scalars().all()
    comp_data = [
        {
            "id": str(c.id),
            "display_name": c.display_name,
            "relationship_mode": c.relationship_mode,
            "companion_gender_presentation": c.companion_gender_presentation,
            "personality_overrides": c.personality_overrides,
            "is_default": c.is_default,
        }
        for c in companions
    ]

    # 4. Conversations and messages
    conv_stmt = select(Conversation).where(Conversation.user_id == user.id)
    conversations = (await db.execute(conv_stmt)).scalars().all()
    conv_data = []
    for conv in conversations:
        msg_stmt = (
            select(Message)
            .where(Message.conversation_id == conv.id)
            .order_by(Message.sequence_no.asc())
        )
        msgs = (await db.execute(msg_stmt)).scalars().all()
        conv_data.append({
            "id": str(conv.id),
            "title": conv.title,
            "conversation_type": conv.conversation_type,
            "created_at": conv.created_at.isoformat() if conv.created_at else None,
            "messages": [
                {
                    "sequence_no": m.sequence_no,
                    "role": m.role,
                    "content": m.content_json,
                    "created_at": m.created_at.isoformat() if m.created_at else None,
                }
                for m in msgs
            ],
        })

    # 5. Memories
    mem_stmt = select(MemoryItem).where(
        MemoryItem.user_id == user.id,
        MemoryItem.status != "deleted",
    )
    memories = (await db.execute(mem_stmt)).scalars().all()
    mem_data = [
        {
            "id": str(m.id),
            "content_text": m.content_text,
            "memory_type": m.memory_type,
            "importance": m.importance,
            "scope": m.scope,
            "created_at": m.created_at.isoformat() if m.created_at else None,
        }
        for m in memories
    ]

    # 6. Media assets
    media_stmt = select(MediaAsset).where(MediaAsset.user_id == user.id)
    media_assets = (await db.execute(media_stmt)).scalars().all()
    media_data = [
        {
            "id": str(a.id),
            "media_type": a.media_type,
            "status": a.status,
            "prompt_text": a.prompt_text,
            "created_at": a.created_at.isoformat() if a.created_at else None,
        }
        for a in media_assets
    ]

    # 7. Credit account
    credit_stmt = select(CreditAccount).where(CreditAccount.user_id == user.id)
    credit_acc = (await db.execute(credit_stmt)).scalar_one_or_none()
    credit_data = {
        "available_balance": credit_acc.available_balance if credit_acc else 0,
        "reserved_balance": credit_acc.reserved_balance if credit_acc else 0,
        "credit_unit": credit_acc.credit_unit if credit_acc else "credits",
    } if credit_acc else None

    return UserDataExportResponse(
        user={
            "id": str(user.id),
            "display_name": user.display_name,
            "preferred_language": user.preferred_language,
            "timezone": user.timezone,
            "age_assurance_status": user.age_assurance_status,
            "created_at": user.created_at.isoformat() if user.created_at else None,
        },
        preferences=pref_data,
        consent_records=consent_data,
        companions=comp_data,
        conversations=conv_data,
        memories=mem_data,
        media_assets=media_data,
        credits=credit_data,
        exported_at=datetime.utcnow(),
    )


@router.delete("/me")
async def delete_my_account(
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Permanently deletes user account and cascades through all related records
    (conversations, messages, memories, generation jobs, media, billing, preferences).
    Adheres to PRD MEM-11, GDPR right to erasure, and SECURITY.md policies.
    """
    user_id = user.id

    # 1. Delete Media, Reservations & Jobs
    await db.execute(delete(CreditReservation).where(CreditReservation.user_id == user_id))
    await db.execute(delete(GenerationJob).where(GenerationJob.user_id == user_id))
    await db.execute(delete(MediaAsset).where(MediaAsset.user_id == user_id))

    # 2. Delete Messages & Summaries for user's conversations
    conv_ids_stmt = select(Conversation.id).where(Conversation.user_id == user_id)
    conv_ids_res = await db.execute(conv_ids_stmt)
    conv_ids = conv_ids_res.scalars().all()
    if conv_ids:
        await db.execute(delete(Message).where(Message.conversation_id.in_(conv_ids)))
        await db.execute(delete(ConversationSummary).where(ConversationSummary.conversation_id.in_(conv_ids)))

    # 3. Delete Conversations & Memories
    await db.execute(delete(Conversation).where(Conversation.user_id == user_id))
    await db.execute(delete(MemoryItem).where(MemoryItem.user_id == user_id))

    # 4. Delete Billing
    await db.execute(delete(CreditLedgerEntry).where(CreditLedgerEntry.user_id == user_id))
    await db.execute(delete(CreditAccount).where(CreditAccount.user_id == user_id))

    # 5. Delete Companions
    await db.execute(delete(CompanionProfile).where(CompanionProfile.user_id == user_id))

    # 6. Delete Preferences, Consent & External Identities
    await db.execute(delete(UserPreference).where(UserPreference.user_id == user_id))
    await db.execute(delete(ConsentRecord).where(ConsentRecord.user_id == user_id))
    await db.execute(delete(ExternalIdentity).where(ExternalIdentity.user_id == user_id))

    # 7. Delete User Record
    await db.execute(delete(User).where(User.id == user_id))
    await db.commit()

    return {
        "status": "deleted",
        "message": "User account and all associated personal data have been permanently removed.",
        "user_id": str(user_id),
    }
