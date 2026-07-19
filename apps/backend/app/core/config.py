from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Implementr API"
    app_env: str = "development"
    app_debug: bool = True

    api_v1_prefix: str = "/api/v1"

    groq_api_key: str = ""
    openai_api_key: str = ""

    log_level: str = "INFO"

    database_url: str = ""

    clerk_publishable_key: str = ""

    clerk_secret_key: str = ""

    clerk_jwt_key: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = Settings()
