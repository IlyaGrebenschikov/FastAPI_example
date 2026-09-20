import logging
from dataclasses import dataclass
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

log = logging.getLogger(__name__)


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


class DatabaseSettings(EnvSettings):
    model_config = SettingsConfigDict(env_prefix="DB_")

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
        return self.url_obj.render_as_string(hide_password=False)


class ServerSettings(EnvSettings):
    model_config = SettingsConfigDict(env_prefix="SERVER_")

    host: str | None = "0.0.0.0"
    port: int | None = 8080


class JWTSettings(EnvSettings):
    model_config = SettingsConfigDict(env_prefix="JWT_")

    algorithm: str = "RS256"
    access_expiration: int = 30
    refresh_expiration: int = 60 * 24 * 30
    certs_dir: str = ""

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
        if self.certs_dir:
            return Path(self.certs_dir)
        return Path(__file__).parents[3] / ".certs"


class CacheSettings(EnvSettings):
    model_config = SettingsConfigDict(env_prefix="CACHE_")

    host: str
    port: int
    password: str | None = None

    @property
    def url(self) -> str:
        password = f":{self.password}@" if self.password else ""
        return f"redis://{password}{self.host}:{self.port}"


class EmailVerifierSettings(EnvSettings):
    model_config = SettingsConfigDict(env_prefix="EMAIL_VERIFIER_")

    api_key: str = ""
    enabled: bool = True


class MessageBrokerSettings(EnvSettings):
    model_config = SettingsConfigDict(env_prefix="MESSAGE_BROKER_")

    host: str = "localhost"
    port: int = 9092

    @property
    def url(self) -> str:
        return f"{self.host}:{self.port}"


class SMTPSettings(EnvSettings):
    model_config = SettingsConfigDict(env_prefix="SMTP_")

    host: str = "localhost"
    port: int = 1025
    use_tls: bool = False
    sender: str = "root@localhost"
    username: str | None = None
    password: str | None = None


@dataclass
class Settings:
    database: DatabaseSettings
    server: ServerSettings
    jwt: JWTSettings
    cache: CacheSettings
    email_verifier: EmailVerifierSettings
    message_broker: MessageBrokerSettings
    smtp: SMTPSettings

    @property
    def root_dir(self) -> Path:
        return Path(__file__).parents[3]


def load_settings() -> Settings:
    log.debug("Loading .env settings.")
    return Settings(
        database=DatabaseSettings(),  # type: ignore[call-arg]
        server=ServerSettings(),
        jwt=JWTSettings(),
        cache=CacheSettings(),  # type: ignore[call-arg]
        email_verifier=EmailVerifierSettings(),
        message_broker=MessageBrokerSettings(),
        smtp=SMTPSettings(),
    )


def load_db_settings() -> DatabaseSettings:
    return DatabaseSettings()  # type: ignore[call-arg]
