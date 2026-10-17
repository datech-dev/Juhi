import uuid

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.domain.models.media import MediaAsset
from app.infrastructure.database.base import Base
from app.infrastructure.database.session import get_db
from app.infrastructure.providers.audio.tts_provider import VeniceTTSProvider
from app.main import app

TEST_DB_URL = "sqlite+aiosqlite:///file:test_milestone6_audio?mode=memory&cache=shared&uri=true"


@pytest.fixture
async def async_engine():
    engine = create_async_engine(
        TEST_DB_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def db_session(async_engine):
    session_factory = async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with session_factory() as session:
        yield session


@pytest.fixture
async def client(async_engine):
    session_factory = async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async def override_get_db():
        async with session_factory() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_venice_tts_provider_mock_fallback():
    provider = VeniceTTSProvider(api_key="")
    result = await provider.synthesize_speech(
        text="Hello! This is Juhi speaking to you with warmth.",
        voice_id="juhi-warm",
    )
    assert result.b64_audio is not None
    assert result.mime_type == "audio/mp3"
    assert result.duration_seconds > 0
    assert result.voice_id == "juhi-warm"


@pytest.mark.asyncio
async def test_direct_speech_synthesis_endpoint(client: AsyncClient):
    headers = {"Authorization": "Bearer test-firebase-token-m6-speech"}
    await client.post("/api/v1/auth/sync", headers=headers)

    res = await client.post(
        "/api/v1/audio/speak",
        headers=headers,
        json={"text": "Vanakkam! Epdi irukinga?", "voice_id": "juhi-warm"},
    )
    assert res.status_code == 200
    data = res.json()
    assert "b64_audio" in data
    assert data["mime_type"] == "audio/mp3"
    assert data["duration_seconds"] > 0
    assert data["voice_id"] == "juhi-warm"


@pytest.mark.asyncio
async def test_message_speech_synthesis_and_asset(client: AsyncClient, db_session: AsyncSession):
    headers = {"Authorization": "Bearer test-firebase-token-m6-msg"}
    await client.post("/api/v1/auth/sync", headers=headers)

    # 1. Create a conversation
    conv_res = await client.post("/api/v1/conversations", headers=headers, json={"title": "Voice Test"})
    conv_id = conv_res.json()["id"]

    # 2. Send a user message to get an assistant message
    turn_res = await client.post(
        f"/api/v1/conversations/{conv_id}/messages",
        headers=headers,
        json={"text": "Can you tell me a short joke?"},
    )
    assert turn_res.status_code == 200
    assistant_msg_id = turn_res.json()["assistant_message"]["id"]

    # 3. Synthesize speech for this assistant message
    speak_res = await client.post(
        f"/api/v1/audio/conversations/{conv_id}/messages/{assistant_msg_id}/speak",
        headers=headers,
        json={"voice_id": "juhi-warm"},
    )
    assert speak_res.status_code == 200
    speak_data = speak_res.json()
    assert "b64_audio" in speak_data
    assert speak_data["asset_id"] is not None

    # 4. Verify MediaAsset is persisted
    asset_id = uuid.UUID(speak_data["asset_id"])
    asset = (await db_session.execute(select(MediaAsset).where(MediaAsset.id == asset_id))).scalar_one_or_none()
    assert asset is not None
    assert asset.asset_kind == "audio"
    assert asset.mime_type == "audio/mp3"


@pytest.mark.asyncio
async def test_audio_cross_user_isolation(client: AsyncClient):
    headers_a = {"Authorization": "Bearer test-firebase-token-m6-usera"}
    headers_b = {"Authorization": "Bearer test-firebase-token-m6-userb"}

    # User A creates a conversation & message
    conv_res = await client.post("/api/v1/conversations", headers=headers_a, json={"title": "Private Chat"})
    conv_id = conv_res.json()["id"]

    turn_res = await client.post(
        f"/api/v1/conversations/{conv_id}/messages",
        headers=headers_a,
        json={"text": "Secret note"},
    )
    msg_id = turn_res.json()["assistant_message"]["id"]

    # User B attempts to synthesize speech on User A's message -> 404
    forbidden_res = await client.post(
        f"/api/v1/audio/conversations/{conv_id}/messages/{msg_id}/speak",
        headers=headers_b,
        json={"voice_id": "juhi-warm"},
    )
    assert forbidden_res.status_code == 404
