import logging

from dishka import AsyncContainer, make_async_container

from fastapi_example.application.dependencies import (
    AuthFeaturesProvider,
    ServicesProvider,
    UsersFeaturesProvider,
)
from fastapi_example.infrastructure.dependencies import (
    CacheProvider,
    CacheRepositoriesProvider,
    CommunicationProvider,
    DatabaseProvider,
    HTTPClientsProvider,
    MessageBrokerProducersProvider,
    MessageBrokerProvider,
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
        CacheProvider(settings.cache),
        CacheRepositoriesProvider(settings.jwt),
        ServicesProvider(settings.smtp),
        UsersFeaturesProvider(),
        AuthFeaturesProvider(settings.jwt),
        HTTPClientsProvider(settings.email_verifier),
        MessageBrokerProvider(settings.message_broker),
        CommunicationProvider(settings.smtp),
        MessageBrokerProducersProvider(),
    )

    return container
