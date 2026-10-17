import logging

from app.core.config import settings
from app.infrastructure.providers.llm.base import BaseLLMProvider
from app.infrastructure.providers.llm.mock_provider import MockLLMProvider
from app.infrastructure.providers.llm.venice_provider import VeniceLLMProvider

logger = logging.getLogger(__name__)


def get_llm_provider() -> BaseLLMProvider:
    provider = settings.AI_PROVIDER.lower()

    if provider == "venice":
        if settings.VENICE_API_KEY:
            return VeniceLLMProvider(
                api_key=settings.VENICE_API_KEY,
                base_url=settings.VENICE_BASE_URL,
                model_name=settings.AI_MODEL,
            )
        logger.warning(
            "AI_PROVIDER is set to 'venice' but VENICE_API_KEY is not configured. Falling back to MockLLMProvider."
        )
        return MockLLMProvider(model_name=f"mock-{settings.AI_MODEL}")

    if provider == "mock":
        return MockLLMProvider(model_name=settings.AI_MODEL)

    return MockLLMProvider(model_name=settings.AI_MODEL)
