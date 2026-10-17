import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from app.infrastructure.database.base import Base

if TYPE_CHECKING:
    from app.domain.models.billing import CreditAccount
    from app.domain.models.companion import CompanionProfile
    from app.domain.models.conversation import Conversation
    from app.domain.models.memory import MemoryItem

# Cross-database JSON type helper
JsonType = JSON().with_variant(JSONB, "postgresql")


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    status: Mapped[str] = mapped_column(String(32), default="active", nullable=False)
    display_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    preferred_language: Mapped[str] = mapped_column(String(16), default="en", nullable=False)
    timezone: Mapped[str] = mapped_column(String(64), default="Asia/Kolkata", nullable=False)
    age_assurance_status: Mapped[str] = mapped_column(String(32), default="unknown", nullable=False)
    age_assurance_reference: Mapped[str | None] = mapped_column(String(255), nullable=True)
    deletion_requested_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relationships
    identities: Mapped[list["ExternalIdentity"]] = relationship(
        "ExternalIdentity", back_populates="user", cascade="all, delete-orphan"
    )
    preferences: Mapped["UserPreference | None"] = relationship(
        "UserPreference", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    consent_records: Mapped[list["ConsentRecord"]] = relationship(
        "ConsentRecord", back_populates="user", cascade="all, delete-orphan"
    )
    companions: Mapped[list["CompanionProfile"]] = relationship(
        "CompanionProfile", back_populates="user"
    )
    conversations: Mapped[list["Conversation"]] = relationship(
        "Conversation", back_populates="user"
    )
    memories: Mapped[list["MemoryItem"]] = relationship("MemoryItem", back_populates="user")
    credit_account: Mapped["CreditAccount | None"] = relationship(
        "CreditAccount", back_populates="user", uselist=False
    )


class ExternalIdentity(Base):
    __tablename__ = "external_identities"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    provider: Mapped[str] = mapped_column(String(32), default="firebase", nullable=False)
    provider_subject: Mapped[str] = mapped_column(String(255), nullable=False)
    email_snapshot: Mapped[str | None] = mapped_column(String(255), nullable=True)
    email_verified: Mapped[bool | None] = mapped_column(Boolean, default=False, nullable=True)
    linked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    last_authenticated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    __table_args__ = (
        UniqueConstraint("provider", "provider_subject", name="uq_provider_subject"),
        Index("ix_external_identities_user", "user_id"),
    )

    user: Mapped["User"] = relationship("User", back_populates="identities")


class UserPreference(Base):
    __tablename__ = "user_preferences"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), primary_key=True
    )
    ui_language: Mapped[str] = mapped_column(String(16), default="en", nullable=False)
    preferred_reply_language: Mapped[str] = mapped_column(
        String(32), default="match_user", nullable=False
    )
    code_switching_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    timezone: Mapped[str] = mapped_column(String(64), default="Asia/Kolkata", nullable=False)
    theme_mode: Mapped[str] = mapped_column(String(16), default="system", nullable=False)
    accessibility_json: Mapped[dict] = mapped_column(JsonType, default=dict, nullable=False)
    memory_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    memory_pause_until: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    image_autoplay_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    voice_reply_mode: Mapped[str] = mapped_column(String(32), default="off", nullable=False)
    relationship_preferences: Mapped[dict] = mapped_column(JsonType, default=dict, nullable=False)
    boundary_preferences: Mapped[dict] = mapped_column(JsonType, default=dict, nullable=False)
    settings_json: Mapped[dict] = mapped_column(JsonType, default=dict, nullable=False)
    schema_version: Mapped[int] = mapped_column(default=1, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="preferences")


class ConsentRecord(Base):
    __tablename__ = "consent_records"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    purpose: Mapped[str] = mapped_column(String(64), nullable=False)
    decision: Mapped[str] = mapped_column(
        String(32), nullable=False
    )  # granted, withdrawn, declined
    notice_version: Mapped[str] = mapped_column(String(32), nullable=False)
    capture_channel: Mapped[str] = mapped_column(String(32), default="app", nullable=False)
    metadata_json: Mapped[dict] = mapped_column("metadata", JsonType, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        Index("ix_consent_records_user_purpose_time", "user_id", "purpose", "created_at"),
    )

    user: Mapped["User"] = relationship("User", back_populates="consent_records")
