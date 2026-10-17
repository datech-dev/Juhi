import uuid
import logging
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.memory.extractor import MemoryExtractor

logger = logging.getLogger(__name__)


class ExtractMemoryTaskPayload(BaseModel):
    user_id: uuid.UUID
    conversation_id: uuid.UUID
    source_message_id: uuid.UUID
    user_text: str
    assistant_text: str


async def handle_extract_memory_task(
    payload: ExtractMemoryTaskPayload,
    db: AsyncSession,
) -> dict:
    logger.info(f"Processing memory extraction for user={payload.user_id}, conv={payload.conversation_id}")
    extractor = MemoryExtractor()
    items = await extractor.extract_and_persist(
        user_id=payload.user_id,
        conversation_id=payload.conversation_id,
        source_message_id=payload.source_message_id,
        user_text=payload.user_text,
        assistant_text=payload.assistant_text,
        db=db,
    )
    return {
        "status": "success",
        "extracted_count": len(items),
        "items": [str(i.id) for i in items],
    }
