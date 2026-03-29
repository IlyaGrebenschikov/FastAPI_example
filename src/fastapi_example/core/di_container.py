import logging

from dishka import AsyncContainer, make_async_container

from fastapi_example.application.di_providers.services import (
    AuthServiceProvider,
    RateLimiterServiceProvider,
    UsersServiceProvider,
)
from fastapi_example.infrastructure.di_providers import (
    CacheProvider,
    DatabaseProvider,
    HasherProvider,
    MappersProvider,
    RepositoriesProvider,
)

from .settings import Settings

log = logging.getLogger(__name__)


def setup_di_container(
    settings: Settings,
) -> AsyncContainer:
    log.debug("Setting up DI container.")
    container = make_async_container(
        DatabaseProvider(settings.infrastructure.database),
        MappersProvider(),
        RepositoriesProvider(),
        UsersServiceProvider(),
        HasherProvider(),
        AuthServiceProvider(settings.infrastructure.jwt),
        CacheProvider(settings.infrastructure.redis),
        RateLimiterServiceProvider(),
    )

    return container
