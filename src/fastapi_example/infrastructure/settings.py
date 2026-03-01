import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from pydantic import computed_field
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


class JWTSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="JWT_",
        extra="ignore"
    )
    algorithm: str = "RS256"
    expiration: int = 30

    @computed_field
    @property
    def private_key(self) -> str:
        return self._get_key_file("jwt-private.pem")

    @computed_field
    @property
    def public_key(self) -> str:
        return self._get_key_file("jwt-public.pem")

    def _get_key_file(self, filename: str) -> str:
        key_path = self._get_certs_path() / filename
        if not key_path.exists():
            raise FileNotFoundError(f"JWT key file not found: {key_path}")

        return key_path.read_text(encoding="utf-8")

    def _get_certs_path(self) -> Path:
        return Path(__file__).parents[3] / ".certs"


@dataclass
class InfrastructureSettings:
    database: DatabaseSettings
    server: UvicornServerSettings
    jwt: JWTSettings


def load_infrastructure_settings(
        database_settings: Optional[DatabaseSettings] = None,
        server_settings: Optional[UvicornServerSettings] = None,
        jwt_settings: Optional[JWTSettings] = None,
    ) -> InfrastructureSettings:
    log.debug("Loading infrastructure settings.")
    return InfrastructureSettings(
        database=database_settings or DatabaseSettings(),
        server=server_settings or UvicornServerSettings(),
        jwt=jwt_settings or JWTSettings(),
    )
