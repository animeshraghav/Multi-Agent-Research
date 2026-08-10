from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application configuration."""

    # ==================================================
    # API KEYS
    # ==================================================

    google_api_key: str = Field(
        ...,
        alias="GOOGLE_API_KEY"
    )
    tavily_api_key: str = Field(
        ...,
        alias="TAVILY_API_KEY"
    )

    # ==================================================
    # LLM CONFIGURATION
    # ==================================================

    gemini_model: str = "gemini-3.6-flash"
    temperature: float = 0.0

    # ==================================================
    # TAVILY CONFIGURATION
    # ==================================================

    tavily_max_results: int = 5

    # ==================================================
    # SCRAPER CONFIGURATION
    # ==================================================

    scraper_timeout: int = 10
    scraper_max_content_length: int = 6000

    # ==================================================
    # PYDANTIC SETTINGS
    # ==================================================

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )


@lru_cache
def get_settings() -> Settings:
    """Return a cached settings instance."""
    return Settings()


settings = get_settings()