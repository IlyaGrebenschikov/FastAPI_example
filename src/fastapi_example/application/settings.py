import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from pydantic import computed_field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

log = logging.getLogger(__name__)


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
        return Path(__file__).parent.parent.parent / ".certs"


@dataclass
class ApplicationSettings:
    jwt: JWTSettings


def load_application_settings(jwt_settings: Optional[JWTSettings] = None) -> ApplicationSettings:
    log.debug("Loading application settings.")
    return ApplicationSettings(jwt=jwt_settings or JWTSettings())
