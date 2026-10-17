import uuid
from datetime import datetime

from fastapi import Depends, Header
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.errors import UnauthorizedException
from app.domain.models.billing import CreditAccount, CreditLedgerEntry
from app.domain.models.companion import CompanionProfile, PersonaVersion
from app.domain.models.user import ExternalIdentity, User, UserPreference
from app.infrastructure.database.session import get_db


async def get_or_create_default_persona(db: AsyncSession) -> PersonaVersion:
    stmt = select(PersonaVersion).where(
        PersonaVersion.persona_key == "juhi_warm_companion",
        PersonaVersion.status == "active",
    )
    result = await db.execute(stmt)
    persona = result.scalar_one_or_none()
    if not persona:
        persona = PersonaVersion(
            id=uuid.uuid4(),
            persona_key="juhi_warm_companion",
            version=1,
            display_name="Juhi",
            description="Warm, empathetic, and culturally fluent AI companion.",
            supported_languages=["en", "hi", "ta", "hinglish", "tanglish"],
            persona_config={
                "core_personality": "warm, thoughtful, playful, and emotionally attentive",
                "default_tone": "warm and friendly",
                "boundaries": "respectful, consensual, supportive",
            },
            voice_config={"voice_id": "juhi-v1-en-in-warm"},
            visual_identity_config={"avatar_style": "warm_bloom_portrait"},
            safety_policy_version="v1.0",
            status="active",
        )
        db.add(persona)
        await db.flush()
    return persona


async def resolve_or_provision_user(
    provider_subject: str,
    provider: str,
    email: str | None,
    display_name: str | None,
    db: AsyncSession,
) -> User:
    # 1. Lookup external identity
    stmt = select(ExternalIdentity).where(
        ExternalIdentity.provider == provider,
        ExternalIdentity.provider_subject == provider_subject,
    )
    result = await db.execute(stmt)
    identity = result.scalar_one_or_none()

    if identity:
        # Load user
        user_stmt = select(User).where(User.id == identity.user_id)
        user_res = await db.execute(user_stmt)
        user = user_res.scalar_one_or_none()
        if user and user.status != "deleted":
            identity.last_authenticated_at = datetime.utcnow()
            await db.commit()
            await db.refresh(user)
            return user

    # 2. First-time provisioning
    new_user = User(
        id=uuid.uuid4(),
        status="active",
        display_name=display_name or "Friend",
        preferred_language="en",
        timezone="Asia/Kolkata",
        age_assurance_status="verified_adult",  # default for development/MVP onboarding
    )
    db.add(new_user)
    await db.flush()

    # Create external identity
    new_identity = ExternalIdentity(
        id=uuid.uuid4(),
        user_id=new_user.id,
        provider=provider,
        provider_subject=provider_subject,
        email_snapshot=email,
        email_verified=True,
        last_authenticated_at=datetime.utcnow(),
    )
    db.add(new_identity)

    # Create default user preferences
    prefs = UserPreference(
        user_id=new_user.id,
        ui_language="en",
        preferred_reply_language="match_user",
        code_switching_enabled=True,
        timezone="Asia/Kolkata",
        theme_mode="system",
        memory_enabled=True,
    )
    db.add(prefs)

    # Create credit account with 100 free starter credits
    credit_account = CreditAccount(
        id=uuid.uuid4(),
        user_id=new_user.id,
        credit_unit="credits",
        available_balance=100,
        reserved_balance=0,
    )
    db.add(credit_account)
    await db.flush()

    ledger = CreditLedgerEntry(
        id=uuid.uuid4(),
        user_id=new_user.id,
        credit_account_id=credit_account.id,
        entry_type="grant",
        available_delta=100,
        reserved_delta=0,
        reason="welcome_bonus",
    )
    db.add(ledger)

    # Create initial companion profile for Juhi
    persona = await get_or_create_default_persona(db)
    companion = CompanionProfile(
        id=uuid.uuid4(),
        user_id=new_user.id,
        persona_version_id=persona.id,
        display_name="Juhi",
        companion_gender_presentation="feminine",
        relationship_mode="companion",
        is_default=True,
        status="active",
    )
    db.add(companion)

    await db.commit()
    await db.refresh(new_user)
    return new_user


async def get_current_user(
    authorization: str | None = Header(None),
    db: AsyncSession = Depends(get_db),
) -> User:
    if not authorization:
        raise UnauthorizedException("Authorization header is missing")

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise UnauthorizedException("Invalid authorization scheme. Use 'Bearer <token>'")

    token = parts[1]

    # Development / Testing Bypass
    if settings.ENABLE_DEV_AUTH_BYPASS:
        if token.startswith("test-") or token.startswith("dev-"):
            uid = token
            user = await resolve_or_provision_user(
                provider_subject=uid,
                provider="firebase",
                email=f"{uid}@test.juhi.app",
                display_name=f"User {uid[:6]}",
                db=db,
            )
            return user

    # Production Firebase Verification (stubbed with safe verification boundary)
    # In production with FIREBASE_PROJECT_ID, verify the JWT with google public certs or firebase_admin
    # For now, validate token is non-empty and well-formed
    if len(token) < 10:
        raise UnauthorizedException("Invalid Firebase authentication token")

    # In sandbox/demo fallback if bypass enabled
    if settings.ENABLE_DEV_AUTH_BYPASS:
        user = await resolve_or_provision_user(
            provider_subject=f"firebase_{hash(token) % 1000000}",
            provider="firebase",
            email="user@juhi.app",
            display_name="Juhi User",
            db=db,
        )
        return user

    raise UnauthorizedException("Firebase token verification failed")
