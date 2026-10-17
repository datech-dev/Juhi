import logging
import uuid

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.authorization import get_current_active_user
from app.core.errors import NotFoundException
from app.domain.media.service import MediaService
from app.domain.models.media import GenerationJob, MediaAsset
from app.domain.models.user import User
from app.infrastructure.database.session import get_db
from app.schemas.media import (
    GenerationJobResponse,
    ImageGenerateRequest,
    MediaAssetResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Media & Image Generation"])


def get_media_service() -> MediaService:
    return MediaService()


async def _run_job_task(job_id: uuid.UUID, service: MediaService):
    try:
        await service.execute_job(job_id)
    except Exception as e:
        logger.error(f"Error executing background image generation job {job_id}: {e}")


@router.post("/images/generate", response_model=GenerationJobResponse)
async def generate_image(
    data: ImageGenerateRequest,
    background_tasks: BackgroundTasks,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
    service: MediaService = Depends(get_media_service),
):
    job = await service.request_image_generation(
        user_id=user.id,
        prompt=data.prompt,
        idempotency_key=data.idempotency_key,
        conversation_id=data.conversation_id,
        db=db,
        model=data.model,
        width=data.width,
        height=data.height,
    )

    # If job was just created and is in queued status, run in background
    if job.status == "queued":
        background_tasks.add_task(_run_job_task, job.id, service)

    return job


@router.get("/jobs/{job_id}", response_model=GenerationJobResponse)
async def get_job_status(
    job_id: uuid.UUID,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(GenerationJob).where(
        GenerationJob.id == job_id,
        GenerationJob.user_id == user.id,
    )
    res = await db.execute(stmt)
    job = res.scalar_one_or_none()
    if not job:
        raise NotFoundException(f"Job {job_id} not found")
    return job


@router.get("/media/{asset_id}", response_model=MediaAssetResponse)
async def get_media_asset(
    asset_id: uuid.UUID,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(MediaAsset).where(
        MediaAsset.id == asset_id,
        MediaAsset.user_id == user.id,
        MediaAsset.processing_status != "deleted",
    )
    res = await db.execute(stmt)
    asset = res.scalar_one_or_none()
    if not asset:
        raise NotFoundException("Media asset not found")
    return asset


@router.get("/media", response_model=list[MediaAssetResponse])
async def list_media_assets(
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(MediaAsset)
        .where(
            MediaAsset.user_id == user.id,
            MediaAsset.processing_status != "deleted",
        )
        .order_by(MediaAsset.created_at.desc())
        .limit(50)
    )
    res = await db.execute(stmt)
    return res.scalars().all()
