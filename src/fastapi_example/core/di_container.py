import logging

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from fastapi_example.application.di_providers.services import (
    AuthServiceProvider,
    UsersServiceProvider,
    RateLimiterServiceProvider
)
from fastapi_example.infrastructure.di_providers import (
    DatabaseProvider,
    HasherProvider,
    MappersProvider,
    RepositoriesProvider,
    CacheProvider
)

from .settings import Settings

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
        HasherProvider(),
        AuthServiceProvider(settings.infrastructure.jwt),
        CacheProvider(settings.infrastructure.redis),
        RateLimiterServiceProvider()
    )

    setup_dishka(container=container, app=app)
