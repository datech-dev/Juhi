import uuid
from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.authorization import get_current_active_user, verify_memory_access
from app.domain.models.memory import MemoryItem
from app.domain.models.user import User
from app.infrastructure.database.session import get_db
from app.schemas.memory import MemoryItemCreate, MemoryItemResponse

router = APIRouter(prefix="/memory", tags=["Memory Management"])


@router.get("", response_model=list[MemoryItemResponse])
async def list_memories(
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(MemoryItem)
        .where(
            MemoryItem.user_id == user.id,
            MemoryItem.status == "active",
        )
        .order_by(MemoryItem.importance.desc(), MemoryItem.created_at.desc())
    )
    result = await db.execute(stmt)
    return result.scalars().all()


@router.post("", response_model=MemoryItemResponse)
async def create_memory(
    data: MemoryItemCreate,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    item = MemoryItem(
        id=uuid.uuid4(),
        user_id=user.id,
        memory_type=data.memory_type,
        scope="real_life",
        content_text=data.content_text,
        importance=data.importance,
        source_kind="user_statement",
        user_confirmed=True,
        user_visible=True,
        status="active",
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


@router.delete("/{memory_id}")
async def delete_memory(
    memory: MemoryItem = Depends(verify_memory_access),
    db: AsyncSession = Depends(get_db),
):
    memory.status = "deleted"
    memory.deleted_at = datetime.utcnow()
    await db.commit()
    return {"message": "Memory item deleted successfully", "id": memory.id}
