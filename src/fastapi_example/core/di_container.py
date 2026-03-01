import logging

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from .settings import Settings
from fastapi_example.application.di_providers.services import (
    AuthServiceProvider,
    UsersServiceProvider,
    HasherServiceProvider,
    TokenServiceProvider
)
from fastapi_example.infrastructure.di_providers import (
    DatabaseProvider,
    MappersProvider,
    RepositoriesProvider
)

log = logging.getLogger(__name__)


def setup_dependencies(
        app: FastAPI,
        settings: Settings,
) -> None:
    log.debug("Setting up dependencies.")
    container = make_async_container(
        DatabaseProvider(settings.infrastructure.database),
        MappersProvider(),
        RepositoriesProvider(),
        UsersServiceProvider(),
        HasherServiceProvider(),
        AuthServiceProvider(settings.infrastructure.jwt),
        TokenServiceProvider()
    )

    setup_dishka(container=container, app=app)
