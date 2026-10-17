import json

import httpx
import pytest

from app.infrastructure.providers.llm.base import LLMMessage
from app.infrastructure.providers.llm.venice_provider import VeniceLLMProvider


@pytest.mark.asyncio
async def test_venice_generate_response():
    # Mock Venice HTTP response
    mock_response_data = {
        "id": "chatcmpl-venice-test-123",
        "object": "chat.completion",
        "model": "llama-3.3-70b",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "Hello! I am Juhi, powered by Venice.ai open models.",
                },
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": 25,
            "completion_tokens": 15,
            "total_tokens": 40,
        },
    }

    def mock_handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v1/chat/completions"
        assert request.headers["authorization"] == "Bearer mock-venice-key"
        body = json.loads(request.content.decode())
        assert body["model"] == "llama-3.3-70b"
        assert body["venice_parameters"]["include_venice_system_prompt"] is False
        return httpx.Response(200, json=mock_response_data)

    transport = httpx.MockTransport(mock_handler)
    mock_client = httpx.AsyncClient(transport=transport)

    provider = VeniceLLMProvider(
        api_key="mock-venice-key",
        base_url="https://api.venice.ai/api/v1",
        model_name="llama-3.3-70b",
        http_client=mock_client,
    )

    messages = [
        LLMMessage(role="system", content="You are Juhi."),
        LLMMessage(role="user", content="Hello Juhi!"),
    ]

    response = await provider.generate_response(messages)
    assert response.content == "Hello! I am Juhi, powered by Venice.ai open models."
    assert response.model == "llama-3.3-70b"
    assert response.total_tokens == 40


@pytest.mark.asyncio
async def test_venice_stream_response():
    sse_lines = [
        'data: {"choices": [{"delta": {"content": "Hello"}}]}\n\n',
        'data: {"choices": [{"delta": {"content": " from"}}]}\n\n',
        'data: {"choices": [{"delta": {"content": " Venice!"}}]}\n\n',
        "data: [DONE]\n\n",
    ]

    def mock_stream_handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            headers={"content-type": "text/event-stream"},
            content="".join(sse_lines).encode("utf-8"),
        )

    transport = httpx.MockTransport(mock_stream_handler)
    mock_client = httpx.AsyncClient(transport=transport)

    provider = VeniceLLMProvider(
        api_key="mock-venice-key",
        base_url="https://api.venice.ai/api/v1",
        model_name="llama-3.3-70b",
        http_client=mock_client,
    )

    messages = [LLMMessage(role="user", content="Hi!")]

    chunks = []
    async for chunk in provider.stream_response(messages):
        chunks.append(chunk.delta)

    full_text = "".join(chunks)
    assert full_text == "Hello from Venice!"
