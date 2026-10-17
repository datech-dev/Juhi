import uuid

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_or_create_default_persona
from app.core.authorization import get_current_active_user
from app.domain.models.companion import CompanionProfile, PersonaVersion
from app.domain.models.user import User
from app.infrastructure.database.session import get_db
from app.schemas.companion import (
    CompanionProfileCreate,
    CompanionProfileResponse,
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
