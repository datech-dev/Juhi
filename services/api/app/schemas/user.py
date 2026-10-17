import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    status: str
    display_name: str | None = None
    preferred_language: str
    timezone: str
    age_assurance_status: str
    created_at: datetime


class UserPreferenceUpdate(BaseModel):
    ui_language: str | None = None
    preferred_reply_language: str | None = None
    code_switching_enabled: bool | None = None
    timezone: str | None = None
    theme_mode: str | None = None
    memory_enabled: bool | None = None


class UserPreferenceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: uuid.UUID
    ui_language: str
    preferred_reply_language: str
    code_switching_enabled: bool
    timezone: str
    theme_mode: str
    memory_enabled: bool
    updated_at: datetime
