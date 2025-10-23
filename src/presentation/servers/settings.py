import logging
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

log = logging.getLogger(__name__)


class UvicornServerSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="uvicorn_server_",
        extra="ignore"
    )

    host: Optional[str] = "0.0.0.0"
    port: Optional[int] = 8080


class ServerSettings(BaseSettings):
    uvicorn: UvicornServerSettings


def load_server_settings(
    uvicorn: UvicornServerSettings = None,
    ) -> ServerSettings:
    log.info("Loading server settings.")
    return ServerSettings(
        uvicorn=uvicorn or UvicornServerSettings(),
    )
