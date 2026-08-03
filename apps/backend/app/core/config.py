from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Implementr API"
    app_env: str = "development"
    app_debug: bool = True

    api_v1_prefix: str = "/api/v1"

    groq_api_key: str = ""
    openai_api_key: str = ""

    jina_api_key: str = ""
    jina_embedding_model: str = "jina-embeddings-v5-text-small"
    jina_embedding_dimension: int = 1024
    jina_batch_size: int = 128
    jina_retry_count: int = 3

    embedding_provider: str = "local"

    log_level: str = "INFO"

    database_url: str = ""

    clerk_publishable_key: str = ""

    clerk_secret_key: str = ""

    clerk_jwt_key: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()

