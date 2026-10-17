import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    SmallInteger,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.models.user import JsonType
from app.infrastructure.database.base import Base

if TYPE_CHECKING:
    from app.domain.models.user import User


class MemoryItem(Base):
    __tablename__ = "memory_items"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    companion_profile_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("companion_profiles.id", ondelete="RESTRICT"), nullable=True
    )
    conversation_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("conversations.id", ondelete="RESTRICT"), nullable=True
    )
    source_message_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("messages.id", ondelete="RESTRICT"), nullable=True
    )
    supersedes_memory_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("memory_items.id", ondelete="SET NULL"), nullable=True
    )
    memory_type: Mapped[str] = mapped_column(
        String(32), nullable=False
    )  # preference, profile_fact, important_person, goal, event, boundary, correction, story_fact, other
    scope: Mapped[str] = mapped_column(
        String(32), default="real_life", nullable=False
    )  # real_life, interaction_preference, story
    story_session_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True)
    content_text: Mapped[str] = mapped_column(Text, nullable=False)
    attributes: Mapped[dict] = mapped_column(JsonType, default=dict, nullable=False)
    source_kind: Mapped[str] = mapped_column(
        String(32), default="conversation_extraction", nullable=False
    )
    extraction_version: Mapped[str | None] = mapped_column(String(32), nullable=True)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    importance: Mapped[int] = mapped_column(SmallInteger, default=3, nullable=False)
    sensitivity: Mapped[str] = mapped_column(
        String(32), default="normal", nullable=False
    )  # normal, sensitive, restricted
    status: Mapped[str] = mapped_column(
        String(32), default="active", nullable=False
    )  # active, paused, superseded, deleted, expired
    user_visible: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    user_confirmed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    valid_from: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    superseded_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    revision: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        UniqueConstraint("id", "user_id", name="uq_memory_user"),
        Index("ix_memory_items_user_active_type", "user_id", "status", "memory_type"),
    )

    user: Mapped["User"] = relationship("User", back_populates="memories")
