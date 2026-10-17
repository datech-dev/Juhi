import uuid

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.authorization import get_current_active_user, verify_conversation_access
from app.core.errors import NotFoundException
from app.domain.models.companion import CompanionProfile
from app.domain.models.conversation import Conversation, Message
from app.domain.models.user import User
from app.infrastructure.database.session import get_db
from app.schemas.conversation import (
    ConversationCreate,
    ConversationResponse,
    StoryConversationCreate,
)

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


SCENARIO_TEMPLATES = {
    "cafe_rain": "A cozy, quiet cafe in Bangalore during a gentle monsoon evening. Juhi and you are sharing hot filter coffee, watching raindrops slide down the window pane.",
    "stargazing": "Atop the serene hills of Nandi Hills on a cool, clear night, lying under a blanket of stars with a warm flask of tea.",
    "mystery_bookstore": "An antique, hidden second-hand bookstore in the heart of town during a storm, uncovering forgotten letters and old maps.",
    "sci_fi": "An observation deck of an orbital deep-space station watching a distant nebula shimmer in purple and gold.",
}


@router.post("/story", response_model=ConversationResponse)
async def create_story_conversation(
    data: StoryConversationCreate,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Creates an interactive roleplay/story session with an isolated story memory scope.
    """
    # 1. Resolve companion
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
            raise NotFoundException("No active companion found for user.")
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

    scenario_text = (
        data.scenario_prompt
        or SCENARIO_TEMPLATES.get(data.scenario_key)
        or SCENARIO_TEMPLATES["cafe_rain"]
    )
    title = data.title or f"Story: {data.scenario_key.replace('_', ' ').title()}"

    conversation = Conversation(
        id=uuid.uuid4(),
        user_id=user.id,
        companion_profile_id=companion.id,
        active_persona_version_id=companion.persona_version_id,
        title=title,
        conversation_type="roleplay",
        status="active",
        metadata_json={
            "scenario_key": data.scenario_key,
            "scenario_prompt": scenario_text,
            "character_role": data.character_role or companion.display_name,
        },
        next_sequence_no=2,
    )
    db.add(conversation)

    # Initial assistant opener introducing the scene
    opener = Message(
        id=uuid.uuid4(),
        conversation_id=conversation.id,
        sequence_no=1,
        role="assistant",
        status="complete",
        content_json={
            "schema_version": 1,
            "parts": [
                {
                    "type": "text",
                    "text": f"*{scenario_text}*\n\n{companion.display_name} looks over with a warm smile: \"Hey... I'm really glad we're here together. What do you want to do first?\"",
                }
            ],
        },
        idempotency_key=f"opener-{conversation.id}",
    )
    db.add(opener)

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
