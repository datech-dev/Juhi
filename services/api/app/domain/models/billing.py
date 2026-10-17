import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Index,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.models.user import JsonType
from app.infrastructure.database.base import Base

if TYPE_CHECKING:
    from app.domain.models.user import User


class CreditAccount(Base):
    __tablename__ = "credit_accounts"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    credit_unit: Mapped[str] = mapped_column(String(32), default="credits", nullable=False)
    available_balance: Mapped[int] = mapped_column(
        BigInteger, default=100, nullable=False
    )  # 100 free starting credits
    reserved_balance: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    version: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("user_id", "credit_unit", name="uq_user_credit_unit"),
        UniqueConstraint("id", "user_id", name="uq_credit_account_user"),
    )

    user: Mapped["User"] = relationship("User", back_populates="credit_account")
    ledger_entries: Mapped[list["CreditLedgerEntry"]] = relationship(
        "CreditLedgerEntry", back_populates="credit_account", cascade="all, delete-orphan"
    )


class CreditLedgerEntry(Base):
    __tablename__ = "credit_ledger_entries"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    credit_account_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("credit_accounts.id", ondelete="RESTRICT"), nullable=False
    )
    entry_type: Mapped[str] = mapped_column(
        String(32), nullable=False
    )  # grant, reserve, settle, release, refund, expire, adjustment
    available_delta: Mapped[int] = mapped_column(BigInteger, nullable=False)
    reserved_delta: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    reason: Mapped[str] = mapped_column(String(100), nullable=False)
    reference_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True)
    metadata_json: Mapped[dict] = mapped_column("metadata", JsonType, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (Index("ix_credit_ledger_user_time", "user_id", "created_at"),)

    credit_account: Mapped["CreditAccount"] = relationship(
        "CreditAccount", back_populates="ledger_entries"
    )
