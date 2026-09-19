import tomllib
from pathlib import Path

from pydantic import BaseModel, model_validator


class TomlConfig(BaseModel):
    @model_validator(mode="before")
    @classmethod
    def load_from_toml(cls, values: dict) -> dict:
        toml_name = cls.__name__.removesuffix("Config").lower() + ".toml"
        path = Path(__file__).parents[3] / "configs" / toml_name
        toml_data = {}
        if path.exists():
            with open(path, "rb") as f:
                toml_data = tomllib.load(f)
        toml_data.update(values)
        return toml_data


class AppConfig(TomlConfig):
    title: str | None = "FastAPI"
    version: str | None = "0.1.0"
    docs_url: str | None = "/docs"
    redoc_url: str | None = "/redoc"


class CorsConfig(TomlConfig):
    methods: list[str] = ["*"]
    headers: list[str] = ["*"]
    origins: list[str] = ["*"]


def load_configs() -> tuple[AppConfig, CorsConfig]:
    return AppConfig(), CorsConfig()  # type: ignore[call-arg]
