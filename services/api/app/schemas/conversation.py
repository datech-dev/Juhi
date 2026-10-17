import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ConversationCreate(BaseModel):
    companion_profile_id: uuid.UUID | None = None
    title: str | None = None
    conversation_type: str = "chat"


class ConversationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    companion_profile_id: uuid.UUID
    title: str | None = None
    conversation_type: str
    status: str
    last_message_at: datetime | None = None
    created_at: datetime


class MessagePart(BaseModel):
    type: str = "text"
    text: str | None = None
    asset_id: str | None = None
    alt_text: str | None = None


class MessageContentEnvelope(BaseModel):
    schema_version: int = 1
    parts: list[MessagePart]


class SendMessageRequest(BaseModel):
    text: str = Field(min_length=1, max_length=4000)
    idempotency_key: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_message_id: str | None = None


class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    conversation_id: uuid.UUID
    sequence_no: int
    role: str
    status: str
    content_json: dict[str, Any]
    idempotency_key: str
    created_at: datetime


class ChatTurnResponse(BaseModel):
    user_message: MessageResponse
    assistant_message: MessageResponse
