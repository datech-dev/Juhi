import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
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
    from app.domain.models.companion import CompanionProfile
    from app.domain.models.user import User


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    companion_profile_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("companion_profiles.id", ondelete="RESTRICT"), nullable=False
    )
    title: Mapped[str | None] = mapped_column(String(200), nullable=True)
    conversation_type: Mapped[str] = mapped_column(
        String(32), default="chat", nullable=False
    )  # chat, roleplay, journal, voice_session
    status: Mapped[str] = mapped_column(
        String(32), default="active", nullable=False
    )  # active, archived, deleting, deleted
    active_persona_version_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("persona_versions.id", ondelete="RESTRICT"), nullable=False
    )
    story_session_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True)
    next_sequence_no: Mapped[int] = mapped_column(BigInteger, default=1, nullable=False)
    last_message_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    metadata_json: Mapped[dict] = mapped_column("metadata", JsonType, default=dict, nullable=False)
    schema_version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("id", "user_id", name="uq_conversation_user"),
        Index("ix_conversations_user_recent", "user_id", "status", "last_message_at"),
    )

    user: Mapped["User"] = relationship("User", back_populates="conversations")
    companion: Mapped["CompanionProfile"] = relationship(
        "CompanionProfile", back_populates="conversations"
    )
    messages: Mapped[list["Message"]] = relationship(
        "Message",
        back_populates="conversation",
        order_by="Message.sequence_no",
        cascade="all, delete-orphan",
    )
    summaries: Mapped[list["ConversationSummary"]] = relationship(
        "ConversationSummary", back_populates="conversation", cascade="all, delete-orphan"
    )


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    conversation_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("conversations.id", ondelete="RESTRICT"), nullable=False
    )
    sequence_no: Mapped[int] = mapped_column(BigInteger, nullable=False)
    role: Mapped[str] = mapped_column(
        String(32), nullable=False
    )  # user, assistant, system_notice, tool_result
    status: Mapped[str] = mapped_column(
        String(32), default="complete", nullable=False
    )  # accepted, processing, complete, failed, redacted, deleted
    content_json: Mapped[dict] = mapped_column(JsonType, nullable=False)
    content_schema_version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    language_detected: Mapped[str | None] = mapped_column(String(16), nullable=True)
    client_message_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    idempotency_key: Mapped[str] = mapped_column(String(100), nullable=False)
    request_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True)
    reply_to_message_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("messages.id", ondelete="SET NULL"), nullable=True
    )
    model_run_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True)
    safety_state: Mapped[str] = mapped_column(
        String(32), default="not_checked", nullable=False
    )  # not_checked, allowed, transformed, blocked, review_required
    token_usage_json: Mapped[dict] = mapped_column(JsonType, default=dict, nullable=False)
    failure_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    accepted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        UniqueConstraint(
            "conversation_id", "sequence_no", name="uq_messages_conversation_sequence"
        ),
        UniqueConstraint(
            "conversation_id", "idempotency_key", name="uq_messages_conversation_idempotency"
        ),
        Index("ix_messages_conversation_sequence", "conversation_id", "sequence_no"),
    )

    conversation: Mapped["Conversation"] = relationship("Conversation", back_populates="messages")


class ConversationSummary(Base):
    __tablename__ = "conversation_summaries"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    conversation_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("conversations.id", ondelete="RESTRICT"), nullable=False
    )
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    summary_kind: Mapped[str] = mapped_column(
        String(32), default="rolling", nullable=False
    )  # rolling, session_close, recovery, user_requested
    summary_text: Mapped[str] = mapped_column(Text, nullable=False)
    from_sequence_no: Mapped[int] = mapped_column(BigInteger, nullable=False)
    through_sequence_no: Mapped[int] = mapped_column(BigInteger, nullable=False)
    model_key: Mapped[str | None] = mapped_column(String(64), nullable=True)
    prompt_version: Mapped[str | None] = mapped_column(String(32), nullable=True)
    schema_version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("conversation_id", "version", name="uq_conversation_summaries_version"),
        Index("ix_conversation_summaries_latest", "conversation_id", "version"),
    )

    conversation: Mapped["Conversation"] = relationship("Conversation", back_populates="summaries")
