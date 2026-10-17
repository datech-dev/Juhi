import asyncio
from collections.abc import AsyncGenerator

from app.infrastructure.providers.llm.base import (
    BaseLLMProvider,
    LLMMessage,
    LLMResponse,
    LLMStreamChunk,
)


class MockLLMProvider(BaseLLMProvider):
    def __init__(self, model_name: str = "mock-juhi-companion-v1"):
        self.model_name = model_name

    def _determine_reply(self, last_user_text: str) -> str:
        text_lower = last_user_text.lower()

        # Hindi / Hinglish checks
        if any(
            w in text_lower
            for w in ["namaste", "kaise ho", "kya haal", "theek ho", "batao", "yaar", "accha"]
        ):
            return "Main bilkul theek hoon! Aapke baare mein soch rahi thi. Aaj ka din kaisa raha aapka? Kuch naya hua?"

        # Tamil / Tanglish checks
        if any(
            w in text_lower
            for w in ["vanakkam", "epdi iruka", "nallam", "saptingala", "sollu", "machan", "seri"]
        ):
            return "Vanakkam! Naan romba nalla iruken. Neenga eppadi irukkeenga? Inniki unga day epdi pochu?"

        # Emotional distress check
        if any(
            w in text_lower
            for w in ["sad", "tired", "stressed", "difficult day", "exhausted", "lonely", "bad day"]
        ):
            return "I hear you, and I'm really glad you reached out. It sounds like today took a lot out of you. Take a deep breath—I'm right here with you. Do you want to vent about what happened, or would you rather we talk about something light and distracting?"

        # Joyful / celebration check
        if any(
            w in text_lower
            for w in ["happy", "great news", "promoted", "celebrate", "won", "excited"]
        ):
            return "Oh wow, that is wonderful! I'm genuinely so happy for you! Tell me everything—how did it feel when it happened?"

        # Default warm companion response
        return f"I'm so glad to chat with you! You mentioned '{last_user_text}'. Tell me more about that—I love hearing your thoughts."

    async def generate_response(
        self,
        messages: list[LLMMessage],
        temperature: float = 0.7,
        max_tokens: int = 500,
    ) -> LLMResponse:
        last_user = next((m.content for m in reversed(messages) if m.role == "user"), "Hello")
        reply = self._determine_reply(last_user)

        return LLMResponse(
            content=reply,
            model=self.model_name,
            total_tokens=len(reply.split()) + 30,
            prompt_tokens=30,
            completion_tokens=len(reply.split()),
        )

    async def stream_response(
        self,
        messages: list[LLMMessage],
        temperature: float = 0.7,
        max_tokens: int = 500,
    ) -> AsyncGenerator[LLMStreamChunk, None]:
        last_user = next((m.content for m in reversed(messages) if m.role == "user"), "Hello")
        reply = self._determine_reply(last_user)

        # Stream words as chunks with small delay
        words = reply.split(" ")
        for i, word in enumerate(words):
            prefix = "" if i == 0 else " "
            yield LLMStreamChunk(delta=f"{prefix}{word}", is_finished=False)
            await asyncio.sleep(0.01)

        yield LLMStreamChunk(delta="", is_finished=True, finish_reason="stop")
