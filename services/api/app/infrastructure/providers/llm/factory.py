from app.core.config import settings
from app.infrastructure.providers.llm.base import BaseLLMProvider
from app.infrastructure.providers.llm.mock_provider import MockLLMProvider


def get_llm_provider() -> BaseLLMProvider:
    provider = settings.AI_PROVIDER.lower()
    if provider == "mock":
        return MockLLMProvider(model_name=settings.AI_MODEL)

    # Fallback to Mock if API keys are not supplied in current environment
    return MockLLMProvider(model_name=settings.AI_MODEL)
