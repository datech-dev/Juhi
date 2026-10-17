import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MemoryItemCreate(BaseModel):
    content_text: str
    memory_type: str = "profile_fact"  # preference, profile_fact, goal, event, boundary
    importance: int = 3


class MemoryItemUpdate(BaseModel):
    content_text: str | None = None
    memory_type: str | None = None
    importance: int | None = None



class MemoryItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    memory_type: str
    scope: str
    content_text: str
    confidence: float | None = None
    importance: int
    status: str
    user_visible: bool
    created_at: datetime
