import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_memory_lifecycle(client: AsyncClient, auth_headers_user1: dict):
    # Provision user
    await client.post("/api/v1/auth/sync", headers=auth_headers_user1)

    # 1. Create Memory Item
    create_res = await client.post(
        "/api/v1/memory",
        json={
            "content_text": "I work as an Android and Flutter engineer in Bangalore",
            "memory_type": "profile_fact",
            "importance": 5,
        },
        headers=auth_headers_user1,
    )
    assert create_res.status_code == 200
    mem_data = create_res.json()
    assert mem_data["content_text"] == "I work as an Android and Flutter engineer in Bangalore"
    assert mem_data["importance"] == 5
    assert mem_data["status"] == "active"
    mem_id = mem_data["id"]

    # 2. List memories
    list_res = await client.get("/api/v1/memory", headers=auth_headers_user1)
    assert list_res.status_code == 200
    items = list_res.json()
    assert len(items) >= 1
    assert any(i["id"] == mem_id for i in items)

    # 3. Soft delete memory
    del_res = await client.delete(f"/api/v1/memory/{mem_id}", headers=auth_headers_user1)
    assert del_res.status_code == 200

    # 4. Confirm it is no longer in active memories
    list_after_del = await client.get("/api/v1/memory", headers=auth_headers_user1)
    assert list_after_del.status_code == 200
    remaining_items = list_after_del.json()
    assert not any(i["id"] == mem_id for i in remaining_items)
