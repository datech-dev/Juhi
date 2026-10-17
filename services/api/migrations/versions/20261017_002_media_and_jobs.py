"""Add media assets, generation jobs, and credit reservations

Revision ID: 20261017_002
Revises: 20261017_001
Create Date: 2026-10-17 12:00:00.000000

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261017_002"
down_revision: str | None = "20261017_001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # 1. credit_reservations
    op.create_table(
        "credit_reservations",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("credit_account_id", sa.Uuid(), sa.ForeignKey("credit_accounts.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("operation_type", sa.String(32), nullable=False, server_default="image_generation"),
        sa.Column("idempotency_key", sa.String(100), nullable=False),
        sa.Column("reserved_amount", sa.BigInteger(), nullable=False),
        sa.Column("settled_amount", sa.BigInteger(), nullable=True),
        sa.Column("status", sa.String(32), nullable=False, server_default="reserved"),
        sa.Column("tariff_version", sa.String(32), nullable=False, server_default="v1.0"),
        sa.Column("reserved_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("settled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("released_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("user_id", "idempotency_key", name="uq_reservation_user_idempotency"),
    )
    op.create_index("ix_credit_reservations_status", "credit_reservations", ["user_id", "status"])

    # 2. generation_jobs
    op.create_table(
        "generation_jobs",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("conversation_id", sa.Uuid(), sa.ForeignKey("conversations.id", ondelete="RESTRICT"), nullable=True),
        sa.Column("source_message_id", sa.Uuid(), nullable=True),
        sa.Column("job_type", sa.String(32), nullable=False, server_default="image_generation"),
        sa.Column("status", sa.String(32), nullable=False, server_default="queued"),
        sa.Column("idempotency_key", sa.String(100), nullable=False),
        sa.Column("credit_reservation_id", sa.Uuid(), sa.ForeignKey("credit_reservations.id", ondelete="SET NULL"), nullable=True),
        sa.Column("request_config", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("provider_key", sa.String(32), nullable=False, server_default="venice"),
        sa.Column("provider_model", sa.String(64), nullable=False, server_default="fluently-xl"),
        sa.Column("result_json", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("error_message", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.UniqueConstraint("user_id", "idempotency_key", name="uq_generation_job_user_idempotency"),
    )
    op.create_index("ix_generation_jobs_user_status", "generation_jobs", ["user_id", "status"])

    # 3. media_assets
    op.create_table(
        "media_assets",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("conversation_id", sa.Uuid(), sa.ForeignKey("conversations.id", ondelete="RESTRICT"), nullable=True),
        sa.Column("message_id", sa.Uuid(), nullable=True),
        sa.Column("generation_job_id", sa.Uuid(), sa.ForeignKey("generation_jobs.id", ondelete="SET NULL"), nullable=True),
        sa.Column("asset_kind", sa.String(32), nullable=False, server_default="image"),
        sa.Column("origin", sa.String(32), nullable=False, server_default="ai_generated"),
        sa.Column("storage_bucket", sa.String(64), nullable=False, server_default="juhi-private-media"),
        sa.Column("object_key", sa.String(255), nullable=False),
        sa.Column("mime_type", sa.String(64), nullable=False, server_default="image/png"),
        sa.Column("byte_size", sa.BigInteger(), nullable=False, server_default="0"),
        sa.Column("width_px", sa.Integer(), nullable=True),
        sa.Column("height_px", sa.Integer(), nullable=True),
        sa.Column("processing_status", sa.String(32), nullable=False, server_default="ready"),
        sa.Column("moderation_status", sa.String(32), nullable=False, server_default="allowed"),
        sa.Column("visibility", sa.String(32), nullable=False, server_default="private"),
        sa.Column("metadata", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )
    op.create_index("ix_media_assets_user_recent", "media_assets", ["user_id", "created_at"])


def downgrade() -> None:
    op.drop_table("media_assets")
    op.drop_table("generation_jobs")
    op.drop_table("credit_reservations")
