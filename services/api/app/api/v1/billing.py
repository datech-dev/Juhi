from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.authorization import get_current_active_user
from app.domain.models.billing import CreditAccount, CreditLedgerEntry
from app.domain.models.user import User
from app.infrastructure.database.session import get_db
from app.schemas.billing import CreditBalanceResponse, CreditLedgerEntryResponse

router = APIRouter(prefix="/billing", tags=["Billing & Credits"])


@router.get("/balance", response_model=CreditBalanceResponse)
async def get_credit_balance(
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Returns the user's authoritative credit balance and current cost rate cards.
    """
    stmt = select(CreditAccount).where(CreditAccount.user_id == user.id)
    result = await db.execute(stmt)
    account = result.scalar_one_or_none()

    return CreditBalanceResponse(
        user_id=user.id,
        available_balance=account.available_balance if account else 0,
        reserved_balance=account.reserved_balance if account else 0,
        credit_unit=account.credit_unit if account else "credits",
        tier="free",
    )


@router.get("/ledger", response_model=list[CreditLedgerEntryResponse])
async def get_credit_ledger(
    limit: int = 50,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Returns an append-only audit trail of credit transactions (grants, reservations, refunds, settles).
    """
    stmt = (
        select(CreditLedgerEntry)
        .where(CreditLedgerEntry.user_id == user.id)
        .order_by(CreditLedgerEntry.created_at.desc())
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()
