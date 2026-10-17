import uuid

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.errors import ForbiddenException, NotFoundException
from app.domain.models.companion import CompanionProfile
from app.domain.models.conversation import Conversation
from app.domain.models.memory import MemoryItem
from app.domain.models.user import User
from app.infrastructure.database.session import get_db


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.status != "active":
        raise ForbiddenException("User account is not active")
    return current_user


async def verify_conversation_access(
    conversation_id: uuid.UUID,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> Conversation:
    stmt = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == user.id,
        Conversation.status != "deleted",
    )
    result = await db.execute(stmt)
    conversation = result.scalar_one_or_none()
    if not conversation:
        raise NotFoundException("Conversation not found")
    return conversation


async def verify_companion_access(
    companion_id: uuid.UUID,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> CompanionProfile:
    stmt = select(CompanionProfile).where(
        CompanionProfile.id == companion_id,
        CompanionProfile.user_id == user.id,
        CompanionProfile.status != "deleted",
    )
    result = await db.execute(stmt)
    companion = result.scalar_one_or_none()
    if not companion:
        raise NotFoundException("Companion profile not found")
    return companion


async def verify_memory_access(
    memory_id: uuid.UUID,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> MemoryItem:
    stmt = select(MemoryItem).where(
        MemoryItem.id == memory_id,
        MemoryItem.user_id == user.id,
        MemoryItem.status != "deleted",
    )
    result = await db.execute(stmt)
    memory = result.scalar_one_or_none()
    if not memory:
        raise NotFoundException("Memory item not found")
    return memory
