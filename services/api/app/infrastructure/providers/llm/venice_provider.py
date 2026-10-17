import json
from collections.abc import AsyncGenerator

import httpx

from app.core.config import settings
from app.core.errors import JuhiAPIException
from app.infrastructure.providers.llm.base import (
    BaseLLMProvider,
    LLMMessage,
    LLMResponse,
    LLMStreamChunk,
)


class VeniceLLMProvider(BaseLLMProvider):
    """
    Venice.ai LLM Provider.
    Interfaces with Venice's OpenAI-compatible API to run open-source models (Llama 3.3 70B, etc.)
    with zero data retention and privacy preservation.
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        model_name: str | None = None,
        http_client: httpx.AsyncClient | None = None,
    ):
        self.api_key = api_key or settings.VENICE_API_KEY
        self.base_url = (base_url or settings.VENICE_BASE_URL).rstrip("/")
        self.model_name = model_name or settings.VENICE_MODEL or settings.AI_MODEL
        self._custom_client = http_client

    def _get_headers(self) -> dict:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _prepare_payload(
        self,
        messages: list[LLMMessage],
        temperature: float = 0.7,
        max_tokens: int = 800,
        stream: bool = False,
    ) -> dict:
        return {
            "model": self.model_name,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream,
            "venice_parameters": {
                "include_venice_system_prompt": False,
            },
        }

    async def generate_response(
        self,
        messages: list[LLMMessage],
        temperature: float = 0.7,
        max_tokens: int = 800,
    ) -> LLMResponse:
        url = f"{self.base_url}/chat/completions"
        payload = self._prepare_payload(messages, temperature, max_tokens, stream=False)

        client = self._custom_client or httpx.AsyncClient(timeout=45.0)
        try:
            response = await client.post(url, json=payload, headers=self._get_headers())
            if response.status_code != 200:
                raise JuhiAPIException(
                    status_code=502,
                    error_code="VENICE_API_ERROR",
                    message=f"Venice API returned error {response.status_code}: {response.text}",
                )

            data = response.json()
            content = data["choices"][0]["message"]["content"]
            usage = data.get("usage", {})

            return LLMResponse(
                content=content,
                model=data.get("model", self.model_name),
                total_tokens=usage.get("total_tokens", 0),
                prompt_tokens=usage.get("prompt_tokens", 0),
                completion_tokens=usage.get("completion_tokens", 0),
            )
        finally:
            if not self._custom_client:
                await client.aclose()

    async def stream_response(
        self,
        messages: list[LLMMessage],
        temperature: float = 0.7,
        max_tokens: int = 800,
    ) -> AsyncGenerator[LLMStreamChunk, None]:
        url = f"{self.base_url}/chat/completions"
        payload = self._prepare_payload(messages, temperature, max_tokens, stream=True)

        client = self._custom_client or httpx.AsyncClient(timeout=60.0)
        try:
            async with client.stream(
                "POST", url, json=payload, headers=self._get_headers()
            ) as response:
                if response.status_code != 200:
                    error_body = await response.aread()
                    raise JuhiAPIException(
                        status_code=502,
                        error_code="VENICE_STREAM_ERROR",
                        message=f"Venice streaming failed with {response.status_code}: {error_body.decode('utf-8', errors='ignore')}",
                    )

                async for line in response.aiter_lines():
                    line = line.strip()
                    if not line:
                        continue
                    if line.startswith("data: "):
                        data_str = line[6:].strip()
                        if data_str == "[DONE]":
                            yield LLMStreamChunk(delta="", is_finished=True, finish_reason="stop")
                            break
                        try:
                            chunk_data = json.loads(data_str)
                            choice = chunk_data.get("choices", [{}])[0]
                            delta_content = choice.get("delta", {}).get("content", "")
                            finish_reason = choice.get("finish_reason")

                            if delta_content:
                                yield LLMStreamChunk(
                                    delta=delta_content,
                                    is_finished=finish_reason is not None,
                                    finish_reason=finish_reason,
                                )
                        except json.JSONDecodeError:
                            continue
        finally:
            if not self._custom_client:
                await client.aclose()
