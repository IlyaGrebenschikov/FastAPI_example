import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

log = logging.getLogger(__name__)


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_prefix="DB_", extra="ignore"
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
        extra="ignore",
    )

    host: Optional[str] = "0.0.0.0"
    port: Optional[int] = 8080


class JWTSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_prefix="JWT_", extra="ignore"
    )
    algorithm: str = "RS256"
    expiration: int = 30

    @property
    def private_key(self) -> str:
        return self._get_key_file("jwt-private.pem")

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


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="REDIS_",
        extra="ignore",
    )
    host: str
    port: int
    password: Optional[str] = None

    @property
    def url(self) -> str:
        password = f":{self.password}@" if self.password else ""
        return f"redis://{password}{self.host}:{self.port}"


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
        env_file=".env", env_file_encoding="utf-8", env_prefix="CORS_", extra="ignore"
    )
    methods: list[str] = ["*"]
    headers: list[str] = ["*"]
    origins: list[str] = ["*"]


class EmailVerifierSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="EMAIL_VERIFIER_",
        extra="ignore",
    )
    api_key: str


@dataclass
class InfrastructureSettings:
    database: DatabaseSettings
    server: UvicornServerSettings
    jwt: JWTSettings
    redis: RedisSettings
    app: AppSettings
    cors: CORSSettings
    email_verifier: EmailVerifierSettings


def load_infrastructure_settings(
    database_settings: Optional[DatabaseSettings] = None,
    server_settings: Optional[UvicornServerSettings] = None,
    jwt_settings: Optional[JWTSettings] = None,
    redis_settings: Optional[RedisSettings] = None,
    app_settings: Optional[AppSettings] = None,
    cors_settings: Optional[CORSSettings] = None,
    email_verifier_settings: Optional[EmailVerifierSettings] = None,
) -> InfrastructureSettings:
    log.debug("Loading infrastructure settings.")
    return InfrastructureSettings(
        database=database_settings or DatabaseSettings(),  # type: ignore[call-arg]
        server=server_settings or UvicornServerSettings(),
        jwt=jwt_settings or JWTSettings(),
        redis=redis_settings or RedisSettings(),  # type: ignore[call-arg]
        app=app_settings or AppSettings(),
        cors=cors_settings or CORSSettings(),
        email_verifier=email_verifier_settings or EmailVerifierSettings(), # type: ignore[call-arg]
    )
