import uuid

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.authorization import get_current_active_user, verify_conversation_access
from app.core.errors import NotFoundException
from app.domain.models.companion import CompanionProfile
from app.domain.models.conversation import Conversation
from app.domain.models.user import User
from app.infrastructure.database.session import get_db
from app.schemas.conversation import ConversationCreate, ConversationResponse

router = APIRouter(prefix="/conversations", tags=["Conversations"])


@router.get("", response_model=list[ConversationResponse])
async def list_conversations(
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(Conversation)
        .where(
            Conversation.user_id == user.id,
            Conversation.status == "active",
        )
        .order_by(Conversation.last_message_at.desc().nulls_last(), Conversation.created_at.desc())
    )
    result = await db.execute(stmt)
    return result.scalars().all()


@router.post("", response_model=ConversationResponse)
async def create_conversation(
    data: ConversationCreate,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    # If no companion_profile_id specified, pick user's default companion
    companion_id = data.companion_profile_id
    if not companion_id:
        comp_stmt = select(CompanionProfile).where(
            CompanionProfile.user_id == user.id,
            CompanionProfile.is_default == True,  # noqa: E712
            CompanionProfile.status == "active",
        )
        comp_res = await db.execute(comp_stmt)
        companion = comp_res.scalar_one_or_none()
        if not companion:
            raise NotFoundException("No active companion found for user. Please create one.")
        companion_id = companion.id
    else:
        comp_stmt = select(CompanionProfile).where(
            CompanionProfile.id == companion_id,
            CompanionProfile.user_id == user.id,
            CompanionProfile.status == "active",
        )
        comp_res = await db.execute(comp_stmt)
        companion = comp_res.scalar_one_or_none()
        if not companion:
            raise NotFoundException("Companion profile not found")

    conversation = Conversation(
        id=uuid.uuid4(),
        user_id=user.id,
        companion_profile_id=companion.id,
        active_persona_version_id=companion.persona_version_id,
        title=data.title or f"Chat with {companion.display_name}",
        conversation_type=data.conversation_type,
        status="active",
        next_sequence_no=1,
    )
    db.add(conversation)
    await db.commit()
    await db.refresh(conversation)
    return conversation


@router.get("/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation: Conversation = Depends(verify_conversation_access),
):
    return conversation


@router.delete("/{conversation_id}")
async def delete_conversation(
    conversation: Conversation = Depends(verify_conversation_access),
    db: AsyncSession = Depends(get_db),
):
    conversation.status = "deleted"
    await db.commit()
    return {"message": "Conversation deleted successfully", "id": conversation.id}
