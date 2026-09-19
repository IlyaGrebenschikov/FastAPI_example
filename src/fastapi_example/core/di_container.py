import logging
from typing import Optional

from dishka import AsyncContainer, make_async_container

from fastapi_example.application.di_providers.services import (
    AuthServiceProvider,
    RateLimiterServiceProvider,
    EmailNotificationsServiceProvider,
)
from fastapi_example.application.di_providers.features import (
    UsersFeaturesProvider,
    AuthFeaturesProvider,
)
from fastapi_example.infrastructure.dependencies import (
    CacheProvider,
    CacheRepositoriesProvider,
    CommunicationProvider,
    DatabaseProvider,
    HTTPClientsProvider,
    MessageBrokerProvider,
    MessageBrokerProducersProvider,
    PwdHasherProvider,
    RepositoriesProvider,
)

from .settings import Settings

log = logging.getLogger(__name__)


def setup_di_container(
    settings: Settings,
) -> AsyncContainer:
    log.debug("Setting up DI container.")
    container = make_async_container(
        DatabaseProvider(settings.database),
        RepositoriesProvider(),
        PwdHasherProvider(),
        AuthServiceProvider(settings.jwt),
        CacheProvider(settings.cache),
        CacheRepositoriesProvider(settings.jwt),
        RateLimiterServiceProvider(),
        UsersFeaturesProvider(),
        AuthFeaturesProvider(),
        HTTPClientsProvider(settings.email_verifier),
        MessageBrokerProvider(settings.message_broker),
        CommunicationProvider(settings.smtp),
        MessageBrokerProducersProvider(),
        EmailNotificationsServiceProvider(),
    )

    return container
