import json
from typing import Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # General
    APP_ENV: str = "development"
    DEBUG: bool = True
    PROJECT_NAME: str = "Juhi AI Companion"
    API_V1_PREFIX: str = "/api/v1"
    SECRET_KEY: str = Field(
        default="development_insecure_secret_key_minimum_32_chars_long_12345",
        min_length=32,
    )
    ALLOWED_ORIGINS: list[str] | str = ["*"]

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Any) -> list[str]:
        if isinstance(v, str):
            if v.startswith("[") and v.endswith("]"):
                try:
                    return json.loads(v)
                except Exception:
                    pass
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, list):
            return [str(i) for i in v]
        return ["*"]

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./juhi_dev.db"
    DB_ECHO: bool = False
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20

    # Authentication & Security
    FIREBASE_PROJECT_ID: str = "juhi-companion"
    ENABLE_DEV_AUTH_BYPASS: bool = True
    DEV_AUTH_SECRET: str = "dev_test_secret_for_local_mocking"
    RATE_LIMIT_PER_MINUTE: int = 60

    # AI Model Providers
    # Primary: venice (privacy-first open models)
    # Options: 'venice', 'mock', 'openai', 'anthropic'
    AI_PROVIDER: str = "venice"
    AI_MODEL: str = "venice-uncensored-role-play"
    VENICE_MODEL: str = "venice-uncensored-role-play"
    VENICE_IMAGE_MODEL: str = "lustify-v7"
    VENICE_BASE_URL: str = "https://api.venice.ai/api/v1"
    VENICE_API_KEY: str | None = None
    OPENAI_API_KEY: str | None = None
    ANTHROPIC_API_KEY: str | None = None


settings = Settings()
