import uuid

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_cross_user_isolation(
    client: AsyncClient, auth_headers_user1: dict, auth_headers_user2: dict
):
    # Provision both users
    await client.post("/api/v1/auth/sync", headers=auth_headers_user1)
    await client.post("/api/v1/auth/sync", headers=auth_headers_user2)

    # User 1 creates a private conversation
    conv_res = await client.post(
        "/api/v1/conversations",
        json={"title": "Alice Secret Chat"},
        headers=auth_headers_user1,
    )
    assert conv_res.status_code == 200
    conv_id = conv_res.json()["id"]

    # User 2 attempts to get User 1's conversation -> MUST fail with 404
    user2_get_res = await client.get(
        f"/api/v1/conversations/{conv_id}",
        headers=auth_headers_user2,
    )
    assert user2_get_res.status_code == 404

    # User 2 attempts to send a message to User 1's conversation -> MUST fail with 404
    user2_post_res = await client.post(
        f"/api/v1/conversations/{conv_id}/messages",
        json={"text": "I am trying to breach your chat", "idempotency_key": str(uuid.uuid4())},
        headers=auth_headers_user2,
    )
    assert user2_post_res.status_code == 404

    # User 2 attempts to list messages of User 1's conversation -> MUST fail with 404
    user2_list_res = await client.get(
        f"/api/v1/conversations/{conv_id}/messages",
        headers=auth_headers_user2,
    )
    assert user2_list_res.status_code == 404


@pytest.mark.asyncio
async def test_memory_isolation(
    client: AsyncClient, auth_headers_user1: dict, auth_headers_user2: dict
):
    # Provision both users
    await client.post("/api/v1/auth/sync", headers=auth_headers_user1)
    await client.post("/api/v1/auth/sync", headers=auth_headers_user2)

    # User 1 adds a private memory
    mem_res = await client.post(
        "/api/v1/memory",
        json={
            "content_text": "I like dark chocolate",
            "memory_type": "preference",
            "importance": 4,
        },
        headers=auth_headers_user1,
    )
    assert mem_res.status_code == 200
    mem_id = mem_res.json()["id"]

    # User 2 deletes User 1's memory -> MUST fail with 404
    del_res = await client.delete(
        f"/api/v1/memory/{mem_id}",
        headers=auth_headers_user2,
    )
    assert del_res.status_code == 404

    # Verify User 1's memory is still intact
    list_res = await client.get("/api/v1/memory", headers=auth_headers_user1)
    assert list_res.status_code == 200
    memories = list_res.json()
    assert any(m["id"] == mem_id for m in memories)
