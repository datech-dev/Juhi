import uuid

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_or_create_default_persona
from app.core.authorization import get_current_active_user
from app.core.errors import NotFoundException
from app.domain.models.companion import CompanionProfile, PersonaVersion
from app.domain.models.user import User
from app.infrastructure.database.session import get_db
from app.schemas.companion import (
    CompanionProfileCreate,
    CompanionProfileResponse,
    CompanionProfileUpdate,
    PersonaVersionResponse,
)

router = APIRouter(prefix="/companions", tags=["Companions & Personas"])


@router.get("/personas", response_model=list[PersonaVersionResponse])
async def list_persona_versions(
    db: AsyncSession = Depends(get_db),
):
    await get_or_create_default_persona(db)
    stmt = select(PersonaVersion).where(PersonaVersion.status == "active")
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/me", response_model=list[CompanionProfileResponse])
async def list_my_companions(
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(CompanionProfile)
        .where(
            CompanionProfile.user_id == user.id,
            CompanionProfile.status == "active",
        )
        .order_by(CompanionProfile.is_default.desc(), CompanionProfile.created_at.asc())
    )
    result = await db.execute(stmt)
    return result.scalars().all()


@router.post("", response_model=CompanionProfileResponse)
async def create_companion_profile(
    data: CompanionProfileCreate,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    # Check persona exists
    persona_stmt = select(PersonaVersion).where(PersonaVersion.id == data.persona_version_id)
    persona_res = await db.execute(persona_stmt)
    persona = persona_res.scalar_one_or_none()
    if not persona:
        persona = await get_or_create_default_persona(db)

    # If this is set as default, unset other defaults
    if data.is_default:
        existing_stmt = select(CompanionProfile).where(
            CompanionProfile.user_id == user.id,
            CompanionProfile.is_default == True,  # noqa: E712
        )
        existing_res = await db.execute(existing_stmt)
        for p in existing_res.scalars().all():
            p.is_default = False

    profile = CompanionProfile(
        id=uuid.uuid4(),
        user_id=user.id,
        persona_version_id=persona.id,
        display_name=data.display_name,
        companion_gender_presentation=data.companion_gender_presentation,
        relationship_mode=data.relationship_mode,
        personality_overrides=data.personality_overrides,
        is_default=data.is_default,
        status="active",
    )
    db.add(profile)
    await db.commit()
    await db.refresh(profile)
    return profile


@router.get("/default", response_model=CompanionProfileResponse)
async def get_default_companion(
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(CompanionProfile)
        .where(
            CompanionProfile.user_id == user.id,
            CompanionProfile.status == "active",
        )
        .order_by(CompanionProfile.is_default.desc(), CompanionProfile.created_at.asc())
        .limit(1)
    )
    result = await db.execute(stmt)
    companion = result.scalar_one_or_none()
    if not companion:
        raise NotFoundException("No active companion profile found")
    return companion


@router.put("/{companion_id}", response_model=CompanionProfileResponse)
async def update_companion_profile(
    companion_id: uuid.UUID,
    data: CompanionProfileUpdate,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(CompanionProfile).where(
        CompanionProfile.id == companion_id,
        CompanionProfile.user_id == user.id,
        CompanionProfile.status == "active",
    )
    result = await db.execute(stmt)
    profile = result.scalar_one_or_none()
    if not profile:
        raise NotFoundException("Companion profile not found")

    if data.display_name is not None:
        profile.display_name = data.display_name
    if data.companion_gender_presentation is not None:
        profile.companion_gender_presentation = data.companion_gender_presentation
    if data.relationship_mode is not None:
        profile.relationship_mode = data.relationship_mode
    if data.personality_overrides is not None:
        profile.personality_overrides = data.personality_overrides
    if data.is_default is True:
        existing_stmt = select(CompanionProfile).where(
            CompanionProfile.user_id == user.id,
            CompanionProfile.is_default == True,  # noqa: E712
        )
        existing_res = await db.execute(existing_stmt)
        for p in existing_res.scalars().all():
            p.is_default = False
        profile.is_default = True

    await db.commit()
    await db.refresh(profile)
    return profile

