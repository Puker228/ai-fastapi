from pathlib import Path
from typing import Literal

from pydantic import (
    HttpUrl,
    PostgresDsn,
    computed_field,
)
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_ignore_empty=True,
        extra="ignore",
    )
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    PROJECT_NAME: str
    SENTRY_DSN: HttpUrl | None = None
    DEBUG: bool = False

    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    AI_BASE_URL: HttpUrl = "http://ollama:11434"
    AI_MODEL: str = "gemma3:4b"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def AI_PULL_URL(self) -> HttpUrl:
        return HttpUrl(f"{self.AI_BASE_URL}api/pull")

    @computed_field  # type: ignore[prop-decorator]
    @property
    def AI_GENERATE_URL(self) -> HttpUrl:
        return HttpUrl(f"{self.AI_BASE_URL}api/generate")


settings = Settings()  # type: ignore
