import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.companion import CompanionProfile
from app.domain.models.conversation import Conversation, Message
from app.domain.models.memory import MemoryItem
from app.domain.models.user import User
from app.domain.orchestration.turn_orchestrator import TurnOrchestrator


@pytest.mark.asyncio
async def test_companion_get_default_and_update(
    client: AsyncClient,
    db_session: AsyncSession,
    auth_headers_user1: dict,
):
    # Initialize user
    await client.post("/api/v1/auth/sync", headers=auth_headers_user1)

    # 1. Fetch default companion
    get_res = await client.get("/api/v1/companions/default", headers=auth_headers_user1)
    assert get_res.status_code == 200
    comp_data = get_res.json()
    assert comp_data["display_name"] == "Juhi"
    assert comp_data["relationship_mode"] == "companion"
    comp_id = comp_data["id"]

    # 2. Update companion profile (e.g. girlfriend relationship mode and playful tone)
    update_payload = {
        "display_name": "Juhi",
        "relationship_mode": "girlfriend",
        "companion_gender_presentation": "feminine",
        "personality_overrides": {
            "tone": "playful and affectionate",
        },
    }
    put_res = await client.put(
        f"/api/v1/companions/{comp_id}",
        json=update_payload,
        headers=auth_headers_user1,
    )
    assert put_res.status_code == 200
    updated = put_res.json()
    assert updated["relationship_mode"] == "girlfriend"
    assert updated["personality_overrides"]["tone"] == "playful and affectionate"


@pytest.mark.asyncio
async def test_memory_search_update_and_clear_all(
    client: AsyncClient,
    db_session: AsyncSession,
    auth_headers_user1: dict,
):
    # Initialize user
    await client.post("/api/v1/auth/sync", headers=auth_headers_user1)

    # 1. Create several memories
    await client.post(
        "/api/v1/memory",
        json={"content_text": "User loves Mysore Pak sweet", "memory_type": "preference", "importance": 4},
        headers=auth_headers_user1,
    )
    await client.post(
        "/api/v1/memory",
        json={"content_text": "User has a golden retriever dog named Simba", "memory_type": "profile_fact", "importance": 5},
        headers=auth_headers_user1,
    )
    item3_res = await client.post(
        "/api/v1/memory",
        json={"content_text": "User is preparing for a marathon in December", "memory_type": "goal", "importance": 3},
        headers=auth_headers_user1,
    )
    item3_id = item3_res.json()["id"]

    # 2. Search memories with query "dog"
    search_res = await client.get("/api/v1/memory?q=dog", headers=auth_headers_user1)
    assert search_res.status_code == 200
    search_data = search_res.json()
    assert len(search_data) == 1
    assert "Simba" in search_data[0]["content_text"]

    # 3. Update memory item
    put_res = await client.put(
        f"/api/v1/memory/{item3_id}",
        json={"content_text": "User finished half-marathon in November", "importance": 5},
        headers=auth_headers_user1,
    )
    assert put_res.status_code == 200
    assert put_res.json()["content_text"] == "User finished half-marathon in November"
    assert put_res.json()["importance"] == 5

    # 4. Clear all memories
    clear_res = await client.delete("/api/v1/memory", headers=auth_headers_user1)
    assert clear_res.status_code == 200
    assert clear_res.json()["count"] >= 3

    # Check list is now empty
    list_res = await client.get("/api/v1/memory", headers=auth_headers_user1)
    assert list_res.status_code == 200
    assert len(list_res.json()) == 0


@pytest.mark.asyncio
async def test_relevance_weighted_context_compilation_and_boundaries(
    db_session: AsyncSession,
):
    orchestrator = TurnOrchestrator()

    # Create user
    user = User(
        id=uuid.uuid4(),
        status="active",
        display_name="Karthik",
        preferred_language="en",
    )
    db_session.add(user)
    await db_session.flush()

    persona_id = uuid.uuid4()
    # Create companion profile
    comp = CompanionProfile(
        id=uuid.uuid4(),
        user_id=user.id,
        persona_version_id=persona_id,
        display_name="Juhi",
        relationship_mode="girlfriend",
        is_default=True,
        status="active",
    )
    db_session.add(comp)

    # Create conversation
    conv = Conversation(
        id=uuid.uuid4(),
        user_id=user.id,
        companion_profile_id=comp.id,
        active_persona_version_id=persona_id,
        title="Chat",
        status="active",
    )
    db_session.add(conv)

    # Add 3 memories: 2 real_life, 1 story
    m1 = MemoryItem(
        id=uuid.uuid4(),
        user_id=user.id,
        content_text="User is a senior software engineer in Bengaluru",
        memory_type="profile_fact",
        scope="real_life",
        importance=3,
        status="active",
    )
    m2 = MemoryItem(
        id=uuid.uuid4(),
        user_id=user.id,
        content_text="User has an energetic pet cat named Luna",
        memory_type="profile_fact",
        scope="real_life",
        importance=2,
        status="active",
    )
    m3 = MemoryItem(
        id=uuid.uuid4(),
        user_id=user.id,
        content_text="In the fantasy world, user is a wizard of Eldoria",
        memory_type="roleplay",
        scope="story",
        importance=5,
        status="active",
    )
    db_session.add_all([m1, m2, m3])

    # Add a user message asking about cat
    msg = Message(
        id=uuid.uuid4(),
        conversation_id=conv.id,
        role="user",
        sequence_no=1,
        idempotency_key=str(uuid.uuid4()),
        content_json={"parts": [{"type": "text", "text": "Can you remind me what my cat is named?"}]},
        status="complete",
    )
    db_session.add(msg)
    await db_session.commit()

    # Compile context
    llm_messages = await orchestrator.compile_context(user, conv, db_session)
    assert len(llm_messages) >= 2
    system_msg = llm_messages[0]
    assert system_msg.role == "system"

    # Check security boundaries & tags
    assert "<remembered_facts>" in system_msg.content
    assert "</remembered_facts>" in system_msg.content
    assert "[SYSTEM BOUNDARY INSTRUCTION]" in system_msg.content

    # Check relevance ranking boosted cat memory over engineer memory despite lower base importance
    lines = system_msg.content.split("\n")
    cat_idx = next(i for i, line in enumerate(lines) if "Luna" in line)
    eng_idx = next(i for i, line in enumerate(lines) if "software engineer" in line)
    assert cat_idx < eng_idx, "Relevance ranking should place query-matched memory before non-matching memory"

    # Check story memory isolation: fantasy wizard should NOT be in real_life conversation
    assert "wizard of Eldoria" not in system_msg.content
