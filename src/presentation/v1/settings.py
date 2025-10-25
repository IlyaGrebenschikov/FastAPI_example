import logging
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

log = logging.getLogger(__name__)


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="APP_",
        extra="ignore",
    )
    
    title: Optional[str] = "FastAPI"
    version: Optional[str] = "0.1.0"
    docs_url: Optional[str] = "/docs"
    redoc_url: Optional[str] = "/redoc"


class CORSSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="CORS_",
        extra="ignore"
    )
    methods: list[str] = ["*"]
    headers: list[str] = ["*"]
    origins: list[str] = ["*"]


class V1APISettings(BaseSettings):
    app: AppSettings
    cors: CORSSettings


def load_v1_api_settings(
    app: AppSettings = None,
    cors: CORSSettings = None,
    ) -> V1APISettings:
    log.info("Loading presentation settings.")
    return V1APISettings(
        app=app or AppSettings(),
        cors=cors or CORSSettings(),
    )
