from pathlib import Path
from typing import Final

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import DirectoryPath
from sqlalchemy import URL


def get_root_dir_path() -> Path:
    return Path(__file__).resolve().parent.parent.parent.parent


class EnvSettings(BaseSettings):
    root_dir_path: DirectoryPath = get_root_dir_path()
    model_config = SettingsConfigDict(
        env_file=f'{root_dir_path}/backend.env',
        env_file_encoding='utf-8',
    )

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    REDIS_HOST: str
    REDIS_PORT: int


class DatabaseSettings(EnvSettings):
    @property
    def get_url_obj(self) -> URL:
        return URL.create(
            'postgresql+asyncpg',
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            database=self.POSTGRES_DB,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT
        )

    @property
    def get_url_str(self) -> str:
        return (
            f'postgresql+asyncpg://'
            f'{self.POSTGRES_USER}:'
            f'{self.POSTGRES_PASSWORD}@'
            f'{self.POSTGRES_HOST}:'
            f'{self.POSTGRES_PORT}/'
            f'{self.POSTGRES_DB}'
        )


class JWTSettings:
    private_key: Final[str] = (get_root_dir_path() / ".certs" / "jwt-private.pem").read_text()
    public_key: Final[str] = (get_root_dir_path() / ".certs" / "jwt-public.pem").read_text()
    algorithm: Final[str] = 'RS256'
    jwt_expiration: Final[int] = 30


class RedisSettings(EnvSettings):
    @property
    def get_url(self) -> str:
        return f'redis://:@{self.REDIS_HOST}:{self.REDIS_PORT}'


def get_db_settings() -> DatabaseSettings:
    return DatabaseSettings()


def get_jwt_settings() -> JWTSettings:
    return JWTSettings()


def get_redis_settings() -> RedisSettings:
    return RedisSettings()
