import base64
import logging
import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import JuhiAPIException, NotFoundException
from app.domain.models.billing import CreditAccount, CreditLedgerEntry
from app.domain.models.media import CreditReservation, GenerationJob, MediaAsset
from app.infrastructure.database import session as db_session_module
from app.infrastructure.providers.image.base import BaseImageProvider
from app.infrastructure.providers.image.venice_image_provider import VeniceImageProvider

logger = logging.getLogger(__name__)

IMAGE_GENERATION_CREDIT_COST = 10


class MediaService:
    def __init__(
        self,
        image_provider: BaseImageProvider | None = None,
        session_factory=None,
    ):
        self.image_provider = image_provider or VeniceImageProvider()
        self.session_factory = session_factory or db_session_module.AsyncSessionLocal

    async def request_image_generation(
        self,
        user_id: uuid.UUID,
        prompt: str,
        idempotency_key: str,
        conversation_id: uuid.UUID | None,
        db: AsyncSession,
        model: str = "lustify-v7",
        width: int = 1024,
        height: int = 1024,
    ) -> GenerationJob:
        # 1. Check idempotency
        stmt = select(GenerationJob).where(
            GenerationJob.user_id == user_id,
            GenerationJob.idempotency_key == idempotency_key,
        )
        res = await db.execute(stmt)
        existing_job = res.scalar_one_or_none()
        if existing_job:
            return existing_job

        # 2. Check and lock credit account
        acct_stmt = (
            select(CreditAccount)
            .where(CreditAccount.user_id == user_id)
            .with_for_update() if not db.bind.url.drivername.startswith("sqlite") else select(CreditAccount).where(CreditAccount.user_id == user_id)
        )
        acct_res = await db.execute(acct_stmt)
        credit_account = acct_res.scalar_one_or_none()

        if not credit_account or credit_account.available_balance < IMAGE_GENERATION_CREDIT_COST:
            raise JuhiAPIException(
                status_code=402,
                error_code="INSUFFICIENT_CREDITS",
                message=f"Image generation requires {IMAGE_GENERATION_CREDIT_COST} credits. Please top up your account.",
            )

        # 3. Create credit reservation
        reservation = CreditReservation(
            id=uuid.uuid4(),
            user_id=user_id,
            credit_account_id=credit_account.id,
            operation_type="image_generation",
            idempotency_key=f"res_{idempotency_key}",
            reserved_amount=IMAGE_GENERATION_CREDIT_COST,
            status="reserved",
            tariff_version="v1.0",
        )
        db.add(reservation)

        # Update credit balance snapshot
        credit_account.available_balance -= IMAGE_GENERATION_CREDIT_COST
        credit_account.reserved_balance += IMAGE_GENERATION_CREDIT_COST
        credit_account.version += 1

        ledger_entry = CreditLedgerEntry(
            id=uuid.uuid4(),
            user_id=user_id,
            credit_account_id=credit_account.id,
            entry_type="reserve",
            available_delta=-IMAGE_GENERATION_CREDIT_COST,
            reserved_delta=IMAGE_GENERATION_CREDIT_COST,
            reason="image_generation_reserve",
            reference_id=reservation.id,
        )
        db.add(ledger_entry)

        # 4. Create generation job
        job = GenerationJob(
            id=uuid.uuid4(),
            user_id=user_id,
            conversation_id=conversation_id,
            job_type="image_generation",
            status="queued",
            idempotency_key=idempotency_key,
            credit_reservation_id=reservation.id,
            request_config={
                "prompt": prompt,
                "width": width,
                "height": height,
                "model": model,
            },
            provider_key="venice",
            provider_model=model,
        )
        db.add(job)
        await db.commit()
        await db.refresh(job)
        return job

    async def execute_job(
        self,
        job_id: uuid.UUID,
        db: AsyncSession | None = None,
    ) -> GenerationJob:
        if db is not None:
            return await self._execute_job_with_session(job_id, db)
        async with self.session_factory() as session:
            return await self._execute_job_with_session(job_id, session)

    async def _execute_job_with_session(
        self,
        job_id: uuid.UUID,
        db: AsyncSession,
    ) -> GenerationJob:
        job_stmt = select(GenerationJob).where(GenerationJob.id == job_id)
        job_res = await db.execute(job_stmt)
        job = job_res.scalar_one_or_none()
        if not job:
            raise NotFoundException(f"Job {job_id} not found")

        # Transition to running
        job.status = "running"
        await db.commit()

        cfg = job.request_config
        prompt = cfg.get("prompt", "Portrait of Juhi")
        width = cfg.get("width", 1024)
        height = cfg.get("height", 1024)
        model = cfg.get("model", "lustify-v7")

        try:
            result = await self.image_provider.generate_image(
                prompt=prompt,
                width=width,
                height=height,
                model=model,
            )

            # Create MediaAsset
            asset_id = uuid.uuid4()
            raw_bytes = base64.b64decode(result.b64_image)
            media_asset = MediaAsset(
                id=asset_id,
                user_id=job.user_id,
                conversation_id=job.conversation_id,
                generation_job_id=job.id,
                asset_kind="image",
                origin="ai_generated",
                storage_bucket="juhi-private-media",
                object_key=f"users/{job.user_id}/images/{asset_id}.png",
                mime_type=result.mime_type,
                byte_size=len(raw_bytes),
                width_px=result.width,
                height_px=result.height,
                processing_status="ready",
                moderation_status="allowed",
                metadata_json={
                    "model": result.model,
                    "b64_preview": result.b64_image,
                },
            )
            db.add(media_asset)

            # Settle reservation
            if job.credit_reservation_id:
                res_stmt = select(CreditReservation).where(CreditReservation.id == job.credit_reservation_id)
                res_res = await db.execute(res_stmt)
                reservation = res_res.scalar_one_or_none()
                if reservation:
                    reservation.status = "settled"
                    reservation.settled_amount = reservation.reserved_amount
                    reservation.settled_at = datetime.utcnow()

                    # Settle in credit account
                    acct_stmt = select(CreditAccount).where(CreditAccount.id == reservation.credit_account_id)
                    acct_res = await db.execute(acct_stmt)
                    credit_account = acct_res.scalar_one_or_none()
                    if credit_account:
                        credit_account.reserved_balance -= reservation.reserved_amount
                        credit_account.version += 1

                        ledger = CreditLedgerEntry(
                            id=uuid.uuid4(),
                            user_id=job.user_id,
                            credit_account_id=credit_account.id,
                            entry_type="settle",
                            available_delta=0,
                            reserved_delta=-reservation.reserved_amount,
                            reason="image_generation_settle",
                            reference_id=reservation.id,
                        )
                        db.add(ledger)

            job.status = "succeeded"
            job.result_json = {
                "asset_id": str(asset_id),
                "mime_type": result.mime_type,
                "model": result.model,
            }
            await db.commit()
            await db.refresh(job)
            return job

        except Exception as e:
            logger.error(f"Image generation job {job_id} failed: {e}")
            # Release reserved credits back to available balance
            if job.credit_reservation_id:
                res_stmt = select(CreditReservation).where(CreditReservation.id == job.credit_reservation_id)
                res_res = await db.execute(res_stmt)
                reservation = res_res.scalar_one_or_none()
                if reservation and reservation.status == "reserved":
                    reservation.status = "released"
                    reservation.released_at = datetime.utcnow()

                    acct_stmt = select(CreditAccount).where(CreditAccount.id == reservation.credit_account_id)
                    acct_res = await db.execute(acct_stmt)
                    credit_account = acct_res.scalar_one_or_none()
                    if credit_account:
                        credit_account.available_balance += reservation.reserved_amount
                        credit_account.reserved_balance -= reservation.reserved_amount
                        credit_account.version += 1

                        ledger = CreditLedgerEntry(
                            id=uuid.uuid4(),
                            user_id=job.user_id,
                            credit_account_id=credit_account.id,
                            entry_type="release",
                            available_delta=reservation.reserved_amount,
                            reserved_delta=-reservation.reserved_amount,
                            reason="image_generation_failed_refund",
                            reference_id=reservation.id,
                        )
                        db.add(ledger)

            job.status = "failed"
            job.error_message = str(e)[:250]
            await db.commit()
            await db.refresh(job)
            return job
