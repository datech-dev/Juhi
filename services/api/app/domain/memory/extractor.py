import json
import logging
import uuid

from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.memory import MemoryItem
from app.infrastructure.providers.llm.base import BaseLLMProvider, LLMMessage
from app.infrastructure.providers.llm.factory import get_llm_provider

logger = logging.getLogger(__name__)


class MemoryCandidate(BaseModel):
    content_text: str = Field(description="Clear, atomic statement of user fact or preference")
    memory_type: str = Field(
        default="profile_fact",
        description="One of: preference, profile_fact, important_person, goal, event, boundary, correction",
    )
    importance: int = Field(default=3, ge=1, le=5)
    confidence: float = Field(default=0.9, ge=0.0, le=1.0)


class MemoryExtractionResult(BaseModel):
    memories: list[MemoryCandidate] = []


EXTRACTION_SYSTEM_PROMPT = """You are a privacy-conscious memory extraction assistant for Juhi AI companion.
Analyze the conversation snippet between the user and Juhi.
Extract any durable personal facts, preferences, life details, goals, or boundaries explicitly mentioned by the user.

Rules:
1. Only extract facts stated by the user about themselves, their preferences, life, family, or work.
2. DO NOT extract temporary small talk (e.g. 'I am eating lunch now').
3. DO NOT extract fictional roleplay claims as real life facts.
4. Output MUST be valid JSON only, matching this structure:
{
  "memories": [
    {
      "content_text": "Prefers speaking in Hinglish when discussing casual topics",
      "memory_type": "preference",
      "importance": 4,
      "confidence": 0.95
    }
  ]
}
If no new durable memories are present, return: {"memories": []}
"""


class MemoryExtractor:
    def __init__(self, provider: BaseLLMProvider | None = None):
        self.provider = provider or get_llm_provider()

    async def extract_and_persist(
        self,
        user_id: uuid.UUID,
        conversation_id: uuid.UUID,
        source_message_id: uuid.UUID,
        user_text: str,
        assistant_text: str,
        db: AsyncSession,
    ) -> list[MemoryItem]:
        # Fast exit for trivial short messages (e.g. "ok", "hi", "thanks")
        if len(user_text.strip().split()) < 3 and not any(
            k in user_text.lower()
            for k in ["like", "love", "work", "live", "am", "hate", "name", "call me"]
        ):
            return []

        prompt_input = (
            f"User message: {user_text}\n"
            f"Assistant response: {assistant_text}\n\n"
            "Extract new durable memories about the user as JSON:"
        )

        messages = [
            LLMMessage(role="system", content=EXTRACTION_SYSTEM_PROMPT),
            LLMMessage(role="user", content=prompt_input),
        ]

        try:
            response = await self.provider.generate_response(
                messages, temperature=0.2, max_tokens=400
            )
            raw_text = response.content.strip()

            # Clean potential markdown fences ```json ... ```
            if raw_text.startswith("```"):
                lines = raw_text.splitlines()
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].startswith("```"):
                    lines = lines[:-1]
                raw_text = "\n".join(lines).strip()

            data = json.loads(raw_text)
            parsed = MemoryExtractionResult.model_validate(data)

            persisted_items: list[MemoryItem] = []
            for candidate in parsed.memories:
                # Check for duplicate recent memory
                dup_stmt = select(MemoryItem).where(
                    MemoryItem.user_id == user_id,
                    MemoryItem.content_text == candidate.content_text,
                    MemoryItem.status == "active",
                )
                dup_res = await db.execute(dup_stmt)
                if dup_res.scalar_one_or_none():
                    continue

                item = MemoryItem(
                    id=uuid.uuid4(),
                    user_id=user_id,
                    conversation_id=conversation_id,
                    source_message_id=source_message_id,
                    memory_type=candidate.memory_type,
                    scope="real_life",
                    content_text=candidate.content_text,
                    importance=candidate.importance,
                    confidence=candidate.confidence,
                    source_kind="conversation_extraction",
                    status="active",
                    user_visible=True,
                    user_confirmed=False,
                )
                db.add(item)
                persisted_items.append(item)

            if persisted_items:
                await db.commit()

            return persisted_items

        except Exception as e:
            logger.warning(f"Memory extraction skipped or failed non-fatally: {e}")
            return []
