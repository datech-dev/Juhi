import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.models.user import JsonType
from app.infrastructure.database.base import Base

if TYPE_CHECKING:
    from app.domain.models.conversation import Conversation
    from app.domain.models.user import User


class PersonaVersion(Base):
    __tablename__ = "persona_versions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    persona_key: Mapped[str] = mapped_column(String(64), nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    display_name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    supported_languages: Mapped[list] = mapped_column(
        JsonType, default=lambda: ["en", "hi", "ta"], nullable=False
    )
    persona_config: Mapped[dict] = mapped_column(JsonType, default=dict, nullable=False)
    voice_config: Mapped[dict] = mapped_column(JsonType, default=dict, nullable=False)
    visual_identity_config: Mapped[dict] = mapped_column(JsonType, default=dict, nullable=False)
    safety_policy_version: Mapped[str] = mapped_column(String(32), default="v1.0", nullable=False)
    status: Mapped[str] = mapped_column(
        String(32), default="active", nullable=False
    )  # draft, active, deprecated, disabled
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_by: Mapped[str | None] = mapped_column(String(100), nullable=True)

    __table_args__ = (
        UniqueConstraint("persona_key", "version", name="uq_persona_version"),
        Index("ix_persona_versions_active", "persona_key", "status"),
    )

    profiles: Mapped[list["CompanionProfile"]] = relationship(
        "CompanionProfile", back_populates="persona_version"
    )


class CompanionProfile(Base):
    __tablename__ = "companion_profiles"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    persona_version_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("persona_versions.id", ondelete="RESTRICT"), nullable=False
    )
    display_name: Mapped[str] = mapped_column(String(100), nullable=False)
    companion_gender_presentation: Mapped[str] = mapped_column(
        String(32), default="feminine", nullable=False
    )
    relationship_mode: Mapped[str] = mapped_column(
        String(32), default="companion", nullable=False
    )  # companion, girlfriend, boyfriend, best_friend, roleplay, custom
    personality_overrides: Mapped[dict] = mapped_column(JsonType, default=dict, nullable=False)
    relationship_preferences: Mapped[dict] = mapped_column(JsonType, default=dict, nullable=False)
    boundaries: Mapped[dict] = mapped_column(JsonType, default=dict, nullable=False)
    visual_identity: Mapped[dict] = mapped_column(JsonType, default=dict, nullable=False)
    voice_preferences: Mapped[dict] = mapped_column(JsonType, default=dict, nullable=False)
    is_default: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    status: Mapped[str] = mapped_column(
        String(32), default="active", nullable=False
    )  # active, archived, deleted
    schema_version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("id", "user_id", name="uq_companion_user"),
        Index("ix_companion_profiles_user_status", "user_id", "status"),
    )

    user: Mapped["User"] = relationship("User", back_populates="companions")
    persona_version: Mapped["PersonaVersion"] = relationship(
        "PersonaVersion", back_populates="profiles"
    )
    conversations: Mapped[list["Conversation"]] = relationship(
        "Conversation", back_populates="companion"
    )
