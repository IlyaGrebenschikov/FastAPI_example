import logging
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

log = logging.getLogger(__name__)


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="app_",
        extra="ignore",
    )
    
    title: Optional[str] = "FastAPI"
    version: Optional[str] = "0.1.0"
    docs_url: Optional[str] = "/docs"
    redoc_url: Optional[str] = "/redoc"


class UvicornServerSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="uvicorn_server_",
        extra="ignore"
    )

    host: Optional[str] = "0.0.0.0"
    port: Optional[int] = 8080


class CORSSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="cors_",
        extra="ignore"
    )
    methods: list[str] = ["*"]
    headers: list[str] = ["*"]
    origins: list[str] = ["*"]


class Settings(BaseSettings):
    app: AppSettings
    cors: CORSSettings
    uvicorn_server: UvicornServerSettings


def load_settings(
    app: AppSettings = None,
    cors: CORSSettings = None,
    uvicorn_server: UvicornServerSettings = None,
    ) -> Settings:
    log.info("Loading presentation settings.")
    return Settings(
        app=app or AppSettings(),
        cors=cors or CORSSettings(),
        uvicorn_server=uvicorn_server or UvicornServerSettings(),
    )
