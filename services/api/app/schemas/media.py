import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ImageGenerateRequest(BaseModel):
    prompt: str = Field(min_length=3, max_length=1000)
    conversation_id: uuid.UUID | None = None
    idempotency_key: str = Field(default_factory=lambda: str(uuid.uuid4()))
    model: str = "fluently-xl"
    width: int = 1024
    height: int = 1024


class GenerationJobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    conversation_id: uuid.UUID | None = None
    job_type: str
    status: str
    idempotency_key: str
    provider_key: str
    provider_model: str
    result_json: dict[str, Any]
    error_message: str | None = None
    created_at: datetime
    updated_at: datetime


class MediaAssetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    conversation_id: uuid.UUID | None = None
    asset_kind: str
    origin: str
    mime_type: str
    byte_size: int
    width_px: int | None = None
    height_px: int | None = None
    processing_status: str
    metadata_json: dict[str, Any]
    created_at: datetime
