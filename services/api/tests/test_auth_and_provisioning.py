import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_auth_sync_provisions_new_user(client: AsyncClient, auth_headers_user1: dict):
    # Call /sync to trigger initial provisioning
    response = await client.post("/api/v1/auth/sync", headers=auth_headers_user1)
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["status"] == "active"
    assert user_data["preferred_language"] == "en"

    # Check credit account was provisioned with 100 starter credits
    credit_res = await client.get("/api/v1/auth/credits", headers=auth_headers_user1)
    assert credit_res.status_code == 200
    credit_data = credit_res.json()
    assert credit_data["available_balance"] == 100
    assert credit_data["credit_unit"] == "credits"

    # Check default companion profile was provisioned
    comp_res = await client.get("/api/v1/companions/me", headers=auth_headers_user1)
    assert comp_res.status_code == 200
    companions = comp_res.json()
    assert len(companions) >= 1
    assert companions[0]["display_name"] == "Juhi"
    assert companions[0]["is_default"] is True


@pytest.mark.asyncio
async def test_unauthorized_access(client: AsyncClient):
    response = await client.get("/api/v1/auth/me")
    assert response.status_code == 401
    data = response.json()
    assert data["error"]["code"] == "UNAUTHORIZED"


@pytest.mark.asyncio
async def test_preferences_update(client: AsyncClient, auth_headers_user1: dict):
    # First sync
    await client.post("/api/v1/auth/sync", headers=auth_headers_user1)

    # Update preferences
    update_payload = {
        "ui_language": "hi",
        "preferred_reply_language": "hinglish",
        "theme_mode": "dark",
        "memory_enabled": True,
    }
    put_res = await client.put(
        "/api/v1/auth/preferences", json=update_payload, headers=auth_headers_user1
    )
    assert put_res.status_code == 200
    prefs = put_res.json()
    assert prefs["ui_language"] == "hi"
    assert prefs["preferred_reply_language"] == "hinglish"
    assert prefs["theme_mode"] == "dark"
