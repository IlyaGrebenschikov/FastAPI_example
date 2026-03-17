from dataclasses import dataclass
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


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


@dataclass
class V1APISettings:
    app: AppSettings
    cors: CORSSettings


def load_v1_api_settings(
        app_settings: Optional[AppSettings] = None,
        cors_settings: Optional[CORSSettings] = None,
) -> V1APISettings:
    return V1APISettings(
        app=app_settings or AppSettings(),
        cors=cors_settings or CORSSettings(),
    )
