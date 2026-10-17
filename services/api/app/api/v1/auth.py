from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.authorization import get_current_active_user
from app.domain.models.billing import CreditAccount
from app.domain.models.user import User, UserPreference
from app.infrastructure.database.session import get_db
from app.schemas.user import UserPreferenceResponse, UserPreferenceUpdate, UserResponse

router = APIRouter(prefix="/auth", tags=["Auth & Profile"])


@router.post("/sync", response_model=UserResponse)
async def sync_user_profile(
    user: User = Depends(get_current_active_user),
):
    """
    Syncs the user profile on login or token refresh and provisions defaults.
    """
    return user


@router.get("/me", response_model=UserResponse)
async def get_my_profile(
    user: User = Depends(get_current_active_user),
):
    return user


@router.get("/preferences", response_model=UserPreferenceResponse)
async def get_my_preferences(
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(UserPreference).where(UserPreference.user_id == user.id)
    result = await db.execute(stmt)
    prefs = result.scalar_one_or_none()
    return prefs


@router.put("/preferences", response_model=UserPreferenceResponse)
async def update_my_preferences(
    update_data: UserPreferenceUpdate,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(UserPreference).where(UserPreference.user_id == user.id)
    result = await db.execute(stmt)
    prefs = result.scalar_one_or_none()

    if update_data.ui_language is not None:
        prefs.ui_language = update_data.ui_language
    if update_data.preferred_reply_language is not None:
        prefs.preferred_reply_language = update_data.preferred_reply_language
    if update_data.code_switching_enabled is not None:
        prefs.code_switching_enabled = update_data.code_switching_enabled
    if update_data.timezone is not None:
        prefs.timezone = update_data.timezone
    if update_data.theme_mode is not None:
        prefs.theme_mode = update_data.theme_mode
    if update_data.memory_enabled is not None:
        prefs.memory_enabled = update_data.memory_enabled

    await db.commit()
    await db.refresh(prefs)
    return prefs


@router.get("/credits")
async def get_credit_balance(
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(CreditAccount).where(CreditAccount.user_id == user.id)
    result = await db.execute(stmt)
    account = result.scalar_one_or_none()
    return {
        "user_id": user.id,
        "available_balance": account.available_balance if account else 0,
        "reserved_balance": account.reserved_balance if account else 0,
        "credit_unit": account.credit_unit if account else "credits",
    }
