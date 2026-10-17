from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator

from pydantic import BaseModel, Field


class LLMMessage(BaseModel):
    role: str = Field(description="Role: 'system', 'user', or 'assistant'")
    content: str


class LLMResponse(BaseModel):
    content: str
    model: str
    total_tokens: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0


class LLMStreamChunk(BaseModel):
    delta: str
    is_finished: bool = False
    finish_reason: str | None = None


class BaseLLMProvider(ABC):
    @abstractmethod
    async def generate_response(
        self,
        messages: list[LLMMessage],
        temperature: float = 0.7,
        max_tokens: int = 500,
    ) -> LLMResponse:
        pass

    @abstractmethod
    async def stream_response(
        self,
        messages: list[LLMMessage],
        temperature: float = 0.7,
        max_tokens: int = 500,
    ) -> AsyncGenerator[LLMStreamChunk, None]:
        pass
