"""Initial schema for Juhi AI Companion core domain

Revision ID: 20261017_001
Revises:
Create Date: 2026-10-17 11:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261017_001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # 1. users
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("status", sa.String(32), nullable=False, server_default="active"),
        sa.Column("display_name", sa.String(100), nullable=True),
        sa.Column("preferred_language", sa.String(16), nullable=False, server_default="en"),
        sa.Column("timezone", sa.String(64), nullable=False, server_default="Asia/Kolkata"),
        sa.Column("age_assurance_status", sa.String(32), nullable=False, server_default="unknown"),
        sa.Column("age_assurance_reference", sa.String(255), nullable=True),
        sa.Column("deletion_requested_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
    )

    # 2. external_identities
    op.create_table(
        "external_identities",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "user_id", sa.Uuid(), sa.ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
        ),
        sa.Column("provider", sa.String(32), nullable=False, server_default="firebase"),
        sa.Column("provider_subject", sa.String(255), nullable=False),
        sa.Column("email_snapshot", sa.String(255), nullable=True),
        sa.Column("email_verified", sa.Boolean(), nullable=True, server_default="0"),
        sa.Column(
            "linked_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("last_authenticated_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("provider", "provider_subject", name="uq_provider_subject"),
    )
    op.create_index("ix_external_identities_user", "external_identities", ["user_id"])

    # 3. user_preferences
    op.create_table(
        "user_preferences",
        sa.Column(
            "user_id", sa.Uuid(), sa.ForeignKey("users.id", ondelete="RESTRICT"), primary_key=True
        ),
        sa.Column("ui_language", sa.String(16), nullable=False, server_default="en"),
        sa.Column(
            "preferred_reply_language", sa.String(32), nullable=False, server_default="match_user"
        ),
        sa.Column("code_switching_enabled", sa.Boolean(), nullable=False, server_default="1"),
        sa.Column("timezone", sa.String(64), nullable=False, server_default="Asia/Kolkata"),
        sa.Column("theme_mode", sa.String(16), nullable=False, server_default="system"),
        sa.Column("accessibility_json", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("memory_enabled", sa.Boolean(), nullable=False, server_default="1"),
        sa.Column("memory_pause_until", sa.DateTime(timezone=True), nullable=True),
        sa.Column("image_autoplay_enabled", sa.Boolean(), nullable=False, server_default="0"),
        sa.Column("voice_reply_mode", sa.String(32), nullable=False, server_default="off"),
        sa.Column("relationship_preferences", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("boundary_preferences", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("settings_json", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("schema_version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
    )

    # 4. consent_records
    op.create_table(
        "consent_records",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "user_id", sa.Uuid(), sa.ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
        ),
        sa.Column("purpose", sa.String(64), nullable=False),
        sa.Column("decision", sa.String(32), nullable=False),
        sa.Column("notice_version", sa.String(32), nullable=False),
        sa.Column("capture_channel", sa.String(32), nullable=False, server_default="app"),
        sa.Column("metadata", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
    )
    op.create_index(
        "ix_consent_records_user_purpose_time",
        "consent_records",
        ["user_id", "purpose", "created_at"],
    )

    # 5. persona_versions
    op.create_table(
        "persona_versions",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("persona_key", sa.String(64), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("display_name", sa.String(100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("supported_languages", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("persona_config", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("voice_config", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("visual_identity_config", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("safety_policy_version", sa.String(32), nullable=False, server_default="v1.0"),
        sa.Column("status", sa.String(32), nullable=False, server_default="active"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_by", sa.String(100), nullable=True),
        sa.UniqueConstraint("persona_key", "version", name="uq_persona_version"),
    )
    op.create_index("ix_persona_versions_active", "persona_versions", ["persona_key", "status"])

    # 6. companion_profiles
    op.create_table(
        "companion_profiles",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "user_id", sa.Uuid(), sa.ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
        ),
        sa.Column(
            "persona_version_id",
            sa.Uuid(),
            sa.ForeignKey("persona_versions.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("display_name", sa.String(100), nullable=False),
        sa.Column(
            "companion_gender_presentation",
            sa.String(32),
            nullable=False,
            server_default="feminine",
        ),
        sa.Column("relationship_mode", sa.String(32), nullable=False, server_default="companion"),
        sa.Column("personality_overrides", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("relationship_preferences", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("boundaries", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("visual_identity", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("voice_preferences", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("is_default", sa.Boolean(), nullable=False, server_default="1"),
        sa.Column("status", sa.String(32), nullable=False, server_default="active"),
        sa.Column("schema_version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.UniqueConstraint("id", "user_id", name="uq_companion_user"),
    )
    op.create_index(
        "ix_companion_profiles_user_status", "companion_profiles", ["user_id", "status"]
    )

    # 7. conversations
    op.create_table(
        "conversations",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "user_id", sa.Uuid(), sa.ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
        ),
        sa.Column(
            "companion_profile_id",
            sa.Uuid(),
            sa.ForeignKey("companion_profiles.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("title", sa.String(200), nullable=True),
        sa.Column("conversation_type", sa.String(32), nullable=False, server_default="chat"),
        sa.Column("status", sa.String(32), nullable=False, server_default="active"),
        sa.Column(
            "active_persona_version_id",
            sa.Uuid(),
            sa.ForeignKey("persona_versions.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("story_session_id", sa.Uuid(), nullable=True),
        sa.Column("next_sequence_no", sa.BigInteger(), nullable=False, server_default="1"),
        sa.Column("last_message_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("schema_version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.UniqueConstraint("id", "user_id", name="uq_conversation_user"),
    )
    op.create_index(
        "ix_conversations_user_recent", "conversations", ["user_id", "status", "last_message_at"]
    )

    # 8. messages
    op.create_table(
        "messages",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "conversation_id",
            sa.Uuid(),
            sa.ForeignKey("conversations.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("sequence_no", sa.BigInteger(), nullable=False),
        sa.Column("role", sa.String(32), nullable=False),
        sa.Column("status", sa.String(32), nullable=False, server_default="complete"),
        sa.Column("content_json", sa.JSON(), nullable=False),
        sa.Column("content_schema_version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("language_detected", sa.String(16), nullable=True),
        sa.Column("client_message_id", sa.String(100), nullable=True),
        sa.Column("idempotency_key", sa.String(100), nullable=False),
        sa.Column("request_id", sa.Uuid(), nullable=True),
        sa.Column(
            "reply_to_message_id",
            sa.Uuid(),
            sa.ForeignKey("messages.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("model_run_id", sa.Uuid(), nullable=True),
        sa.Column("safety_state", sa.String(32), nullable=False, server_default="not_checked"),
        sa.Column("token_usage_json", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("failure_code", sa.String(64), nullable=True),
        sa.Column(
            "accepted_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.UniqueConstraint(
            "conversation_id", "sequence_no", name="uq_messages_conversation_sequence"
        ),
        sa.UniqueConstraint(
            "conversation_id", "idempotency_key", name="uq_messages_conversation_idempotency"
        ),
    )
    op.create_index(
        "ix_messages_conversation_sequence", "messages", ["conversation_id", "sequence_no"]
    )

    # 9. conversation_summaries
    op.create_table(
        "conversation_summaries",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "conversation_id",
            sa.Uuid(),
            sa.ForeignKey("conversations.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("summary_kind", sa.String(32), nullable=False, server_default="rolling"),
        sa.Column("summary_text", sa.Text(), nullable=False),
        sa.Column("from_sequence_no", sa.BigInteger(), nullable=False),
        sa.Column("through_sequence_no", sa.BigInteger(), nullable=False),
        sa.Column("model_key", sa.String(64), nullable=True),
        sa.Column("prompt_version", sa.String(32), nullable=True),
        sa.Column("schema_version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.UniqueConstraint("conversation_id", "version", name="uq_conversation_summaries_version"),
    )
    op.create_index(
        "ix_conversation_summaries_latest", "conversation_summaries", ["conversation_id", "version"]
    )

    # 10. memory_items
    op.create_table(
        "memory_items",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "user_id", sa.Uuid(), sa.ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
        ),
        sa.Column(
            "companion_profile_id",
            sa.Uuid(),
            sa.ForeignKey("companion_profiles.id", ondelete="RESTRICT"),
            nullable=True,
        ),
        sa.Column(
            "conversation_id",
            sa.Uuid(),
            sa.ForeignKey("conversations.id", ondelete="RESTRICT"),
            nullable=True,
        ),
        sa.Column(
            "source_message_id",
            sa.Uuid(),
            sa.ForeignKey("messages.id", ondelete="RESTRICT"),
            nullable=True,
        ),
        sa.Column(
            "supersedes_memory_id",
            sa.Uuid(),
            sa.ForeignKey("memory_items.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("memory_type", sa.String(32), nullable=False),
        sa.Column("scope", sa.String(32), nullable=False, server_default="real_life"),
        sa.Column("story_session_id", sa.Uuid(), nullable=True),
        sa.Column("content_text", sa.Text(), nullable=False),
        sa.Column("attributes", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column(
            "source_kind", sa.String(32), nullable=False, server_default="conversation_extraction"
        ),
        sa.Column("extraction_version", sa.String(32), nullable=True),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.Column("importance", sa.SmallInteger(), nullable=False, server_default="3"),
        sa.Column("sensitivity", sa.String(32), nullable=False, server_default="normal"),
        sa.Column("status", sa.String(32), nullable=False, server_default="active"),
        sa.Column("user_visible", sa.Boolean(), nullable=False, server_default="1"),
        sa.Column("user_confirmed", sa.Boolean(), nullable=False, server_default="0"),
        sa.Column("valid_from", sa.DateTime(timezone=True), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("superseded_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revision", sa.Integer(), nullable=False, server_default="1"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("id", "user_id", name="uq_memory_user"),
    )
    op.create_index(
        "ix_memory_items_user_active_type", "memory_items", ["user_id", "status", "memory_type"]
    )

    # 11. credit_accounts
    op.create_table(
        "credit_accounts",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "user_id", sa.Uuid(), sa.ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
        ),
        sa.Column("credit_unit", sa.String(32), nullable=False, server_default="credits"),
        sa.Column("available_balance", sa.BigInteger(), nullable=False, server_default="100"),
        sa.Column("reserved_balance", sa.BigInteger(), nullable=False, server_default="0"),
        sa.Column("version", sa.BigInteger(), nullable=False, server_default="0"),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.UniqueConstraint("user_id", "credit_unit", name="uq_user_credit_unit"),
        sa.UniqueConstraint("id", "user_id", name="uq_credit_account_user"),
    )

    # 12. credit_ledger_entries
    op.create_table(
        "credit_ledger_entries",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "user_id", sa.Uuid(), sa.ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
        ),
        sa.Column(
            "credit_account_id",
            sa.Uuid(),
            sa.ForeignKey("credit_accounts.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("entry_type", sa.String(32), nullable=False),
        sa.Column("available_delta", sa.BigInteger(), nullable=False),
        sa.Column("reserved_delta", sa.BigInteger(), nullable=False, server_default="0"),
        sa.Column("reason", sa.String(100), nullable=False),
        sa.Column("reference_id", sa.Uuid(), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
    )
    op.create_index(
        "ix_credit_ledger_user_time", "credit_ledger_entries", ["user_id", "created_at"]
    )


def downgrade() -> None:
    op.drop_table("credit_ledger_entries")
    op.drop_table("credit_accounts")
    op.drop_table("memory_items")
    op.drop_table("conversation_summaries")
    op.drop_table("messages")
    op.drop_table("conversations")
    op.drop_table("companion_profiles")
    op.drop_table("persona_versions")
    op.drop_table("consent_records")
    op.drop_table("user_preferences")
    op.drop_table("external_identities")
    op.drop_table("users")
