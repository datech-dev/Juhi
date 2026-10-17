import uuid
from collections.abc import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.memory.extractor import MemoryExtractor
from app.infrastructure.providers.llm.base import (
    BaseLLMProvider,
    LLMMessage,
    LLMResponse,
    LLMStreamChunk,
)


class MockExtractionLLMProvider(BaseLLMProvider):
    async def generate_response(
        self,
        messages: list[LLMMessage],
        temperature: float = 0.7,
        max_tokens: int = 500,
    ) -> LLMResponse:
        # Returns structured JSON memories
        json_output = """{
            "memories": [
                {
                    "content_text": "Prefers filter coffee over tea in the mornings",
                    "memory_type": "preference",
                    "importance": 4,
                    "confidence": 0.98
                },
                {
                    "content_text": "Works as a senior software architect in Bangalore",
                    "memory_type": "profile_fact",
                    "importance": 5,
                    "confidence": 0.95
                }
            ]
        }"""
        return LLMResponse(content=json_output, model="mock-extractor")

    async def stream_response(
        self,
        messages: list[LLMMessage],
        temperature: float = 0.7,
        max_tokens: int = 500,
    ) -> AsyncGenerator[LLMStreamChunk, None]:
        yield LLMStreamChunk(delta="", is_finished=True)


@pytest.mark.asyncio
async def test_memory_extractor_persists_memories(db_session: AsyncSession):
    mock_provider = MockExtractionLLMProvider()
    extractor = MemoryExtractor(provider=mock_provider)

    user_id = uuid.uuid4()
    conv_id = uuid.uuid4()
    msg_id = uuid.uuid4()

    user_text = (
        "I am a senior software architect living in Bangalore and I always prefer filter coffee."
    )
    assist_text = "That is so cool! Bangalore has the best filter coffee spots."

    items = await extractor.extract_and_persist(
        user_id=user_id,
        conversation_id=conv_id,
        source_message_id=msg_id,
        user_text=user_text,
        assistant_text=assist_text,
        db=db_session,
    )

    assert len(items) == 2
    assert items[0].user_id == user_id
    assert items[0].scope == "real_life"
    assert items[0].source_kind == "conversation_extraction"
    assert items[0].status == "active"
    assert "coffee" in items[0].content_text.lower() or "bangalore" in items[0].content_text.lower()

    # Re-running with same content should deduplicate and return 0 new records
    second_run = await extractor.extract_and_persist(
        user_id=user_id,
        conversation_id=conv_id,
        source_message_id=msg_id,
        user_text=user_text,
        assistant_text=assist_text,
        db=db_session,
    )
    assert len(second_run) == 0


@pytest.mark.asyncio
async def test_memory_extractor_skips_trivial_messages(db_session: AsyncSession):
    extractor = MemoryExtractor()
    items = await extractor.extract_and_persist(
        user_id=uuid.uuid4(),
        conversation_id=uuid.uuid4(),
        source_message_id=uuid.uuid4(),
        user_text="ok thanks",
        assistant_text="You're welcome!",
        db=db_session,
    )
    assert len(items) == 0
