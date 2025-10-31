import logging

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from .settings import Settings
from src.application.di_providers.services import (
    UsersServiceProvider,
    HasherServiceProvider
)
from src.infrastructure.di_providers import DatabaseProvider

log = logging.getLogger(__name__)


def setup_dependencies(
        app: FastAPI,
        settings: Settings,
) -> None:
    log.info("Setting up dependencies.")
    container = make_async_container(
        DatabaseProvider(settings.infrastructure_settings),
        UsersServiceProvider(),
        HasherServiceProvider()
    )

    setup_dishka(container=container, app=app)
