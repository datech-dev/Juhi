import uuid

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_conversation_and_chat_turn(client: AsyncClient, auth_headers_user1: dict):
    # 1. Sync user
    await client.post("/api/v1/auth/sync", headers=auth_headers_user1)

    # 2. Create conversation
    create_conv_res = await client.post(
        "/api/v1/conversations",
        json={"title": "Evening Talk", "conversation_type": "chat"},
        headers=auth_headers_user1,
    )
    assert create_conv_res.status_code == 200
    conv_data = create_conv_res.json()
    conv_id = conv_data["id"]

    # 3. Send message
    msg_idempotency = str(uuid.uuid4())
    send_res = await client.post(
        f"/api/v1/conversations/{conv_id}/messages",
        json={"text": "Hello Juhi! How are you doing today?", "idempotency_key": msg_idempotency},
        headers=auth_headers_user1,
    )
    assert send_res.status_code == 200
    turn_data = send_res.json()
    user_msg = turn_data["user_message"]
    assist_msg = turn_data["assistant_message"]

    assert user_msg["sequence_no"] == 1
    assert user_msg["role"] == "user"
    assert assist_msg["sequence_no"] == 2
    assert assist_msg["role"] == "assistant"
    assert (
        "Juhi" in assist_msg["content_json"]["parts"][0]["text"]
        or len(assist_msg["content_json"]["parts"][0]["text"]) > 0
    )

    # 4. Test Idempotency: re-sending the same idempotency key must return the exact same turn
    repeat_res = await client.post(
        f"/api/v1/conversations/{conv_id}/messages",
        json={"text": "Hello Juhi! How are you doing today?", "idempotency_key": msg_idempotency},
        headers=auth_headers_user1,
    )
    assert repeat_res.status_code == 200
    repeat_turn = repeat_res.json()
    assert repeat_turn["user_message"]["id"] == user_msg["id"]
    assert repeat_turn["assistant_message"]["id"] == assist_msg["id"]
    assert repeat_turn["user_message"]["sequence_no"] == 1
    assert repeat_turn["assistant_message"]["sequence_no"] == 2

    # 5. List messages in conversation
    list_res = await client.get(
        f"/api/v1/conversations/{conv_id}/messages",
        headers=auth_headers_user1,
    )
    assert list_res.status_code == 200
    messages = list_res.json()
    assert len(messages) == 2
    assert messages[0]["sequence_no"] == 1
    assert messages[1]["sequence_no"] == 2


@pytest.mark.asyncio
async def test_multilingual_chat_hinglish(client: AsyncClient, auth_headers_user1: dict):
    await client.post("/api/v1/auth/sync", headers=auth_headers_user1)

    create_conv_res = await client.post(
        "/api/v1/conversations",
        json={"title": "Hinglish Chat"},
        headers=auth_headers_user1,
    )
    conv_id = create_conv_res.json()["id"]

    send_res = await client.post(
        f"/api/v1/conversations/{conv_id}/messages",
        json={"text": "Namaste Juhi! Kaise ho aap?", "idempotency_key": str(uuid.uuid4())},
        headers=auth_headers_user1,
    )
    assert send_res.status_code == 200
    assist_text = send_res.json()["assistant_message"]["content_json"]["parts"][0]["text"]
    assert "theek" in assist_text.lower() or "aap" in assist_text.lower()


@pytest.mark.asyncio
async def test_multilingual_chat_tanglish(client: AsyncClient, auth_headers_user1: dict):
    await client.post("/api/v1/auth/sync", headers=auth_headers_user1)

    create_conv_res = await client.post(
        "/api/v1/conversations",
        json={"title": "Tanglish Chat"},
        headers=auth_headers_user1,
    )
    conv_id = create_conv_res.json()["id"]

    send_res = await client.post(
        f"/api/v1/conversations/{conv_id}/messages",
        json={"text": "Vanakkam Juhi! Epdi iruka?", "idempotency_key": str(uuid.uuid4())},
        headers=auth_headers_user1,
    )
    assert send_res.status_code == 200
    assist_text = send_res.json()["assistant_message"]["content_json"]["parts"][0]["text"]
    assert "vanakkam" in assist_text.lower() or "nalla" in assist_text.lower()


def test_clean_reply_strips_style_tags_and_prefixes():
    from app.domain.orchestration.turn_orchestrator import TurnOrchestrator

    # 1. Test <Style> tag stripping
    raw_reply = "<Style>\nOmg you're so cute! 😭 Let me see your face!"
    cleaned = TurnOrchestrator._clean_reply(raw_reply, "Juhi")
    assert "<Style>" not in cleaned
    assert "<style>" not in cleaned.lower()
    assert "cute" in cleaned

    # 2. Test meta-commentary prefix stripping
    meta_reply = 'Here is my sweet response:\n"Wait, who is she?? 🤨 You better not be flirting without me!"'
    cleaned = TurnOrchestrator._clean_reply(meta_reply, "Juhi")
    assert "Here is" not in cleaned
    assert "Wait, who is she" in cleaned

    # 3. Test character prefix stripping
    prefixed = "Juhi: Of course I do, you're mine! 😤 Tell me rn!"
    cleaned = TurnOrchestrator._clean_reply(prefixed, "Juhi")
    assert not cleaned.startswith("Juhi:")
    assert "mine" in cleaned


@pytest.mark.asyncio
async def test_selfie_request_handling(client: AsyncClient, auth_headers_user1: dict):
    await client.post("/api/v1/auth/sync", headers=auth_headers_user1)

    create_conv_res = await client.post(
        "/api/v1/conversations",
        json={"title": "Selfie Chat"},
        headers=auth_headers_user1,
    )
    conv_id = create_conv_res.json()["id"]

    send_res = await client.post(
        f"/api/v1/conversations/{conv_id}/messages",
        json={"text": "Send me your selfie", "idempotency_key": str(uuid.uuid4())},
        headers=auth_headers_user1,
    )
    assert send_res.status_code == 200
    parts = send_res.json()["assistant_message"]["content_json"]["parts"]
    assert len(parts) >= 1
    # Check that it either attaches an image or responds with a photo caption / request
    assert "selfie" in parts[0]["text"].lower() or "pic" in parts[0]["text"].lower() or len(parts) > 1

