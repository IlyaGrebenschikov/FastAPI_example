from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import DirectoryPath
from sqlalchemy import URL


def get_root_dir_path() -> Path:
    return Path(__file__).resolve().parent.parent.parent.parent.parent


class EnvSettings(BaseSettings):
    root_dir_path: DirectoryPath = get_root_dir_path()
    model_config = SettingsConfigDict(
        env_file=f'{root_dir_path}/.env.user',
        env_file_encoding='utf-8',
    )

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str


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


def get_db_settings() -> DatabaseSettings:
    return DatabaseSettings()
