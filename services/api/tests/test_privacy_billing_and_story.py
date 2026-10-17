import uuid

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.domain.models.conversation import Conversation
from app.domain.models.memory import MemoryItem
from app.domain.models.user import User
from app.infrastructure.database.base import Base
from app.infrastructure.database.session import get_db
from app.main import app

# Shared in-memory SQLite database
TEST_DB_URL = "sqlite+aiosqlite:///file:test_milestone5?mode=memory&cache=shared&uri=true"


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
async def test_user_consent_and_onboarding(client: AsyncClient):
    headers = {"Authorization": "Bearer test-firebase-token-m5-user1"}

    # 1. Sync user
    sync_res = await client.post("/api/v1/auth/sync", headers=headers)
    assert sync_res.status_code == 200

    # 2. Record AI disclosure consent
    consent1 = await client.post(
        "/api/v1/users/me/consent",
        headers=headers,
        json={
            "purpose": "ai_companion_disclosure",
            "decision": "granted",
            "notice_version": "v1.0",
        },
    )
    assert consent1.status_code == 200
    assert consent1.json()["decision"] == "granted"

    # 3. Record 18+ age verification
    consent2 = await client.post(
        "/api/v1/users/me/consent",
        headers=headers,
        json={
            "purpose": "age_verification_18_plus",
            "decision": "granted",
            "notice_version": "v1.0",
        },
    )
    assert consent2.status_code == 200

    # 4. Check user profile reflects verified_adult
    profile_res = await client.get("/api/v1/auth/me", headers=headers)
    assert profile_res.status_code == 200
    assert profile_res.json()["age_assurance_status"] == "verified_adult"

    # 5. Check preferences settings_json
    prefs_res = await client.get("/api/v1/auth/preferences", headers=headers)
    assert prefs_res.status_code == 200


@pytest.mark.asyncio
async def test_billing_balance_and_ledger(client: AsyncClient):
    headers = {"Authorization": "Bearer test-firebase-token-m5-billing"}

    # Sync
    await client.post("/api/v1/auth/sync", headers=headers)

    # 1. Fetch balance
    balance_res = await client.get("/api/v1/billing/balance", headers=headers)
    assert balance_res.status_code == 200
    data = balance_res.json()
    assert data["available_balance"] == 100
    assert data["reserved_balance"] == 0
    assert data["rate_cards"]["image_generation"] == 10

    # 2. Fetch ledger
    ledger_res = await client.get("/api/v1/billing/ledger", headers=headers)
    assert ledger_res.status_code == 200
    entries = ledger_res.json()
    assert len(entries) >= 1
    assert entries[0]["entry_type"] == "grant"
    assert entries[0]["available_delta"] == 100
    assert entries[0]["reason"] == "welcome_bonus"


@pytest.mark.asyncio
async def test_story_conversation_and_context(client: AsyncClient):
    headers = {"Authorization": "Bearer test-firebase-token-m5-story"}

    await client.post("/api/v1/auth/sync", headers=headers)

    # 1. Create a story session
    story_res = await client.post(
        "/api/v1/conversations/story",
        headers=headers,
        json={
            "scenario_key": "cafe_rain",
            "title": "Rainy Cafe Tale",
        },
    )
    assert story_res.status_code == 200
    story_conv = story_res.json()
    assert story_conv["conversation_type"] == "roleplay"
    conv_id = story_conv["id"]

    # 2. Check initial opener message exists
    msgs_res = await client.get(f"/api/v1/conversations/{conv_id}/messages", headers=headers)
    assert msgs_res.status_code == 200
    messages = msgs_res.json()
    assert len(messages) == 1
    assert messages[0]["role"] == "assistant"
    assert "Bangalore" in messages[0]["content_json"]["parts"][0]["text"]

    # 3. Send a message in story conversation
    turn_res = await client.post(
        f"/api/v1/conversations/{conv_id}/messages",
        headers=headers,
        json={"text": "I take a sip of the warm coffee and ask what music you like."},
    )
    assert turn_res.status_code == 200
    turn_data = turn_res.json()
    assert turn_data["assistant_message"]["role"] == "assistant"


@pytest.mark.asyncio
async def test_user_data_export(client: AsyncClient):
    headers = {"Authorization": "Bearer test-firebase-token-m5-export"}

    await client.post("/api/v1/auth/sync", headers=headers)

    # Add a memory
    await client.post(
        "/api/v1/memory",
        headers=headers,
        json={"content_text": "Prefers warm chamomile tea", "memory_type": "preference"},
    )

    # Call export endpoint
    export_res = await client.get("/api/v1/users/me/export", headers=headers)
    assert export_res.status_code == 200
    export_data = export_res.json()

    assert "user" in export_data
    assert "preferences" in export_data
    assert "companions" in export_data
    assert "memories" in export_data
    assert len(export_data["memories"]) >= 1
    assert export_data["memories"][0]["content_text"] == "Prefers warm chamomile tea"
    assert "credits" in export_data
    assert export_data["credits"]["available_balance"] == 100


@pytest.mark.asyncio
async def test_account_deletion_cascade(client: AsyncClient, db_session: AsyncSession):
    headers = {"Authorization": "Bearer test-firebase-token-m5-delete"}

    # Provision user and some data
    sync_res = await client.post("/api/v1/auth/sync", headers=headers)
    user_id = uuid.UUID(sync_res.json()["id"])

    # Create memory
    await client.post(
        "/api/v1/memory",
        headers=headers,
        json={"content_text": "To be forgotten fact", "memory_type": "boundary"},
    )

    # Create story
    story_res = await client.post(
        "/api/v1/conversations/story",
        headers=headers,
        json={"scenario_key": "stargazing"},
    )
    conv_id = uuid.UUID(story_res.json()["id"])

    # Verify data exists before delete
    mem_check = (await db_session.execute(select(MemoryItem).where(MemoryItem.user_id == user_id))).scalars().all()
    assert len(mem_check) >= 1

    # Delete account
    del_res = await client.delete("/api/v1/users/me", headers=headers)
    assert del_res.status_code == 200
    assert del_res.json()["status"] == "deleted"

    # Verify everything was wiped
    user_check = (await db_session.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    assert user_check is None

    mem_after = (await db_session.execute(select(MemoryItem).where(MemoryItem.user_id == user_id))).scalars().all()
    assert len(mem_after) == 0

    conv_after = (await db_session.execute(select(Conversation).where(Conversation.id == conv_id))).scalar_one_or_none()
    assert conv_after is None
