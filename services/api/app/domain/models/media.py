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
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.models.user import JsonType
from app.infrastructure.database.base import Base

if TYPE_CHECKING:
    pass


class CreditReservation(Base):
    __tablename__ = "credit_reservations"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    credit_account_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("credit_accounts.id", ondelete="RESTRICT"), nullable=False)
    operation_type: Mapped[str] = mapped_column(String(32), default="image_generation", nullable=False)
    idempotency_key: Mapped[str] = mapped_column(String(100), nullable=False)
    reserved_amount: Mapped[int] = mapped_column(BigInteger, nullable=False)
    settled_amount: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="reserved", nullable=False)  # reserved, settled, released, expired
    tariff_version: Mapped[str] = mapped_column(String(32), default="v1.0", nullable=False)
    reserved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    settled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    released_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        UniqueConstraint("user_id", "idempotency_key", name="uq_reservation_user_idempotency"),
        Index("ix_credit_reservations_status", "user_id", "status"),
    )


class GenerationJob(Base):
    __tablename__ = "generation_jobs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    conversation_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("conversations.id", ondelete="RESTRICT"), nullable=True)
    source_message_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True)
    job_type: Mapped[str] = mapped_column(String(32), default="image_generation", nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="queued", nullable=False)  # queued, reserved, running, succeeded, failed, cancelled
    idempotency_key: Mapped[str] = mapped_column(String(100), nullable=False)
    credit_reservation_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("credit_reservations.id", ondelete="SET NULL"), nullable=True)
    request_config: Mapped[dict] = mapped_column(JsonType, default=dict, nullable=False)
    provider_key: Mapped[str] = mapped_column(String(32), default="venice", nullable=False)
    provider_model: Mapped[str] = mapped_column(String(64), default="fluently-xl", nullable=False)
    result_json: Mapped[dict] = mapped_column(JsonType, default=dict, nullable=False)
    error_message: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "idempotency_key", name="uq_generation_job_user_idempotency"),
        Index("ix_generation_jobs_user_status", "user_id", "status"),
    )

    media_asset: Mapped["MediaAsset | None"] = relationship("MediaAsset", back_populates="generation_job", uselist=False)


class MediaAsset(Base):
    __tablename__ = "media_assets"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    conversation_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("conversations.id", ondelete="RESTRICT"), nullable=True)
    message_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True)
    generation_job_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("generation_jobs.id", ondelete="SET NULL"), nullable=True)
    asset_kind: Mapped[str] = mapped_column(String(32), default="image", nullable=False)  # image, audio, video, sticker
    origin: Mapped[str] = mapped_column(String(32), default="ai_generated", nullable=False)
    storage_bucket: Mapped[str] = mapped_column(String(64), default="juhi-private-media", nullable=False)
    object_key: Mapped[str] = mapped_column(String(255), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(64), default="image/png", nullable=False)
    byte_size: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    width_px: Mapped[int | None] = mapped_column(Integer, nullable=True)
    height_px: Mapped[int | None] = mapped_column(Integer, nullable=True)
    processing_status: Mapped[str] = mapped_column(String(32), default="ready", nullable=False)  # pending, ready, failed, deleted
    moderation_status: Mapped[str] = mapped_column(String(32), default="allowed", nullable=False)
    visibility: Mapped[str] = mapped_column(String(32), default="private", nullable=False)
    metadata_json: Mapped[dict] = mapped_column("metadata", JsonType, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        Index("ix_media_assets_user_recent", "user_id", "created_at"),
    )

    generation_job: Mapped["GenerationJob | None"] = relationship("GenerationJob", back_populates="media_asset")
