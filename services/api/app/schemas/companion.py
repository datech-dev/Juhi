import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class PersonaVersionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    persona_key: str
    version: int
    display_name: str
    description: str | None = None
    supported_languages: list[str]
    status: str


class CompanionProfileCreate(BaseModel):
    persona_version_id: uuid.UUID
    display_name: str
    companion_gender_presentation: str = "feminine"
    relationship_mode: str = (
        "companion"  # companion, girlfriend, boyfriend, best_friend, roleplay, custom
    )
    personality_overrides: dict[str, Any] = {}
    is_default: bool = True


class CompanionProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    persona_version_id: uuid.UUID
    display_name: str
    companion_gender_presentation: str
    relationship_mode: str
    is_default: bool
    status: str
    created_at: datetime
