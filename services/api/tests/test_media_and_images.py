import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.media import get_media_service
from app.domain.media.service import MediaService
from app.domain.models.billing import CreditAccount
from app.domain.models.media import CreditReservation
from app.infrastructure.providers.image.base import BaseImageProvider, ImageGenerationResult
from app.infrastructure.providers.image.venice_image_provider import MOCK_PNG_B64
from app.main import app as fastapi_app
from tests.conftest import TestSessionLocal


class MockImageProvider(BaseImageProvider):
    def __init__(self, should_fail: bool = False):
        self.should_fail = should_fail

    async def generate_image(self, prompt: str, **kwargs) -> ImageGenerationResult:
        if self.should_fail:
            raise RuntimeError("Provider GPU timeout")
        return ImageGenerationResult(
            b64_image=MOCK_PNG_B64,
            mime_type="image/png",
            width=512,
            height=512,
            model="mock-fluently-xl",
        )


@pytest.mark.asyncio
async def test_image_generation_request_and_job_lifecycle(
    client: AsyncClient,
    db_session: AsyncSession,
    auth_headers_user1: dict,
):
    # Setup mock media service using TestSessionLocal
    mock_service = MediaService(
        image_provider=MockImageProvider(should_fail=False),
        session_factory=TestSessionLocal,
    )
    fastapi_app.dependency_overrides[get_media_service] = lambda: mock_service

    # 1. Trigger auth sync so user and credit account exist
    auth_res = await client.post("/api/v1/auth/sync", headers=auth_headers_user1)
    assert auth_res.status_code == 200
    user_id = uuid.UUID(auth_res.json()["id"])

    # Verify initial credit balance is 100
    acct_stmt = select(CreditAccount).where(CreditAccount.user_id == user_id)
    acct = (await db_session.execute(acct_stmt)).scalar_one()
    assert acct.available_balance == 100
    assert acct.reserved_balance == 0

    # 2. Request image generation
    idempotency_key = str(uuid.uuid4())
    req_payload = {
        "prompt": "Juhi walking under cherry blossoms in spring",
        "idempotency_key": idempotency_key,
        "model": "fluently-xl",
        "width": 1024,
        "height": 1024,
    }
    gen_res = await client.post(
        "/api/v1/images/generate",
        json=req_payload,
        headers=auth_headers_user1,
    )
    assert gen_res.status_code == 200
    job_data = gen_res.json()
    job_id = uuid.UUID(job_data["id"])
    assert job_data["job_type"] == "image_generation"

    # Because FastAPI executes background tasks synchronously at the end of the test request,
    # the job will have executed with our mock_service
    # 3. Query job status endpoint
    job_status_res = await client.get(
        f"/api/v1/jobs/{job_id}",
        headers=auth_headers_user1,
    )
    assert job_status_res.status_code == 200
    status_data = job_status_res.json()
    assert status_data["id"] == str(job_id)
    assert status_data["status"] == "succeeded"
    asset_id = uuid.UUID(status_data["result_json"]["asset_id"])

    # Verify reservation settled
    await db_session.refresh(acct)
    assert acct.available_balance == 90
    assert acct.reserved_balance == 0

    res_stmt = select(CreditReservation).where(CreditReservation.user_id == user_id)
    reservation = (await db_session.execute(res_stmt)).scalar_one()
    assert reservation.status == "settled"
    assert reservation.settled_amount == 10

    # Verify MediaAsset exists and can be retrieved
    media_res = await client.get(
        f"/api/v1/media/{asset_id}",
        headers=auth_headers_user1,
    )
    assert media_res.status_code == 200
    assert media_res.json()["id"] == str(asset_id)
    assert media_res.json()["mime_type"] == "image/png"
    assert media_res.json()["metadata_json"]["b64_preview"] == MOCK_PNG_B64

    # List media assets
    list_res = await client.get("/api/v1/media", headers=auth_headers_user1)
    assert list_res.status_code == 200
    assert len(list_res.json()) >= 1


@pytest.mark.asyncio
async def test_image_generation_failed_refunds_credits(
    client: AsyncClient,
    db_session: AsyncSession,
    auth_headers_user1: dict,
):
    # Setup mock failing service
    failing_service = MediaService(
        image_provider=MockImageProvider(should_fail=True),
        session_factory=TestSessionLocal,
    )
    fastapi_app.dependency_overrides[get_media_service] = lambda: failing_service

    # Initialize user
    auth_res = await client.post("/api/v1/auth/sync", headers=auth_headers_user1)
    user_id = uuid.UUID(auth_res.json()["id"])

    acct_stmt = select(CreditAccount).where(CreditAccount.user_id == user_id)
    acct = (await db_session.execute(acct_stmt)).scalar_one()
    starting_available = acct.available_balance

    # Request generation
    req_payload = {
        "prompt": "A scenic painting of Mumbai marine drive",
        "idempotency_key": str(uuid.uuid4()),
    }
    gen_res = await client.post(
        "/api/v1/images/generate",
        json=req_payload,
        headers=auth_headers_user1,
    )
    job_id = uuid.UUID(gen_res.json()["id"])

    # Job executed in background and failed
    job_status_res = await client.get(
        f"/api/v1/jobs/{job_id}",
        headers=auth_headers_user1,
    )
    assert job_status_res.status_code == 200
    failed_job_data = job_status_res.json()
    assert failed_job_data["status"] == "failed"
    assert "Provider GPU timeout" in failed_job_data["error_message"]

    # Verify credits were refunded (released back to available)
    await db_session.refresh(acct)
    assert acct.available_balance == starting_available
    assert acct.reserved_balance == 0


@pytest.mark.asyncio
async def test_image_generation_insufficient_credits(
    client: AsyncClient,
    db_session: AsyncSession,
    auth_headers_user1: dict,
):
    mock_service = MediaService(
        image_provider=MockImageProvider(should_fail=False),
        session_factory=TestSessionLocal,
    )
    fastapi_app.dependency_overrides[get_media_service] = lambda: mock_service

    # Initialize user
    auth_res = await client.post("/api/v1/auth/sync", headers=auth_headers_user1)
    user_id = uuid.UUID(auth_res.json()["id"])

    # Set available credits to 5 (less than 10)
    acct_stmt = select(CreditAccount).where(CreditAccount.user_id == user_id)
    acct = (await db_session.execute(acct_stmt)).scalar_one()
    acct.available_balance = 5
    await db_session.commit()

    req_payload = {
        "prompt": "An impossible image",
        "idempotency_key": str(uuid.uuid4()),
    }
    gen_res = await client.post(
        "/api/v1/images/generate",
        json=req_payload,
        headers=auth_headers_user1,
    )
    assert gen_res.status_code == 402
    assert "INSUFFICIENT_CREDITS" in gen_res.text


@pytest.mark.asyncio
async def test_media_cross_user_isolation(
    client: AsyncClient,
    db_session: AsyncSession,
    auth_headers_user1: dict,
    auth_headers_user2: dict,
):
    mock_service = MediaService(
        image_provider=MockImageProvider(should_fail=False),
        session_factory=TestSessionLocal,
    )
    fastapi_app.dependency_overrides[get_media_service] = lambda: mock_service

    # Setup user 1 and user 2
    await client.post("/api/v1/auth/sync", headers=auth_headers_user1)
    await client.post("/api/v1/auth/sync", headers=auth_headers_user2)

    # User 1 creates a job
    req_payload = {
        "prompt": "User 1 private portrait",
        "idempotency_key": str(uuid.uuid4()),
    }
    gen_res = await client.post(
        "/api/v1/images/generate",
        json=req_payload,
        headers=auth_headers_user1,
    )
    job_id = uuid.UUID(gen_res.json()["id"])

    # User 2 tries to access User 1's job -> 404
    user2_job_res = await client.get(
        f"/api/v1/jobs/{job_id}",
        headers=auth_headers_user2,
    )
    assert user2_job_res.status_code == 404

    # Get job data for User 1 to find asset_id
    user1_job_res = await client.get(
        f"/api/v1/jobs/{job_id}",
        headers=auth_headers_user1,
    )
    assert user1_job_res.status_code == 200
    asset_id = uuid.UUID(user1_job_res.json()["result_json"]["asset_id"])

    # User 2 tries to access User 1's media asset -> 404
    user2_asset_res = await client.get(
        f"/api/v1/media/{asset_id}",
        headers=auth_headers_user2,
    )
    assert user2_asset_res.status_code == 404

    # User 2's media list does not include User 1's media asset
    user2_list = await client.get("/api/v1/media", headers=auth_headers_user2)
    assert user2_list.status_code == 200
    asset_ids = [item["id"] for item in user2_list.json()]
    assert str(asset_id) not in asset_ids
