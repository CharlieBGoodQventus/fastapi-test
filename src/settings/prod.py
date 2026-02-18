"""Production environment settings using environment variables."""

from pydantic_settings import SettingsConfigDict

from settings.base import SECRETS_PATH, Settings as BaseSettings


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        secrets_dir=str(SECRETS_PATH),
        frozen=True,
        extra="ignore",
        populate_by_name=True,
    )


settings = Settings()
