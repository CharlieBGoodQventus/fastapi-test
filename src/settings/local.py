"""Local environment settings using .env file."""

from pydantic_settings import SettingsConfigDict

from settings.base import Settings as BaseSettings


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        frozen=True,
        extra="ignore",
        populate_by_name=True,
    )


settings = Settings()
