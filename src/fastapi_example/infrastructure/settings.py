import logging
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

log = logging.getLogger(__name__)


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="DB_",
        extra="ignore"
    )
    drivername: str = "postgresql+asyncpg"
    host: str
    port: int
    username: str
    password: str
    database: str

    @property
    def url_obj(self) -> URL:
        return URL.create(**self.model_dump())

    @property
    def url_str(self) -> str:
        return (
            f"{self.drivername}://"
            f"{self.username}:"
            f"{self.password}@"
            f"{self.host}:"
            f"{self.port}/"
            f"{self.database}"
        )


class UvicornServerSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="UVICORN_SERVER_",
        extra="ignore"
    )

    host: Optional[str] = "0.0.0.0"
    port: Optional[int] = 8080


class InfrastructureSettings(BaseSettings):
    database: DatabaseSettings
    server: UvicornServerSettings


def load_infrastructure_settings(
        database: Optional[DatabaseSettings] = None,
        server: Optional[UvicornServerSettings] = None,
    ) -> InfrastructureSettings:
    log.debug("Loading infrastructure settings.")
    return InfrastructureSettings(
        database=database or DatabaseSettings(),
        server=server or UvicornServerSettings(),
    )
