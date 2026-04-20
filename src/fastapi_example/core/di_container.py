import logging

from dishka import AsyncContainer, make_async_container

from fastapi_example.application.di_providers.services import (
    AuthServiceProvider,
    RateLimiterServiceProvider,
    EmailValidatorServiceProvider
)
from fastapi_example.application.di_providers.features import (
    UsersFeaturesProvider,
    AuthFeaturesProvider,
)
from fastapi_example.infrastructure.di_providers import (
    CacheProvider,
    DatabaseProvider,
    HasherProvider,
    CacheRepositoriesProvider,
    DBMappersProvider,
    DBRepositoriesProvider,
    HTTPClientsProvider
)

from .settings import Settings

log = logging.getLogger(__name__)


def setup_di_container(
    settings: Settings,
) -> AsyncContainer:
    log.debug("Setting up DI container.")
    container = make_async_container(
        DatabaseProvider(settings.infrastructure.database),
        DBMappersProvider(),
        DBRepositoriesProvider(),
        HasherProvider(),
        AuthServiceProvider(settings.infrastructure.jwt),
        CacheProvider(settings.infrastructure.redis),
        CacheRepositoriesProvider(),
        RateLimiterServiceProvider(),
        UsersFeaturesProvider(),
        AuthFeaturesProvider(),
        HTTPClientsProvider(settings.infrastructure.email_verifier),
        EmailValidatorServiceProvider(),
    )

    return container
