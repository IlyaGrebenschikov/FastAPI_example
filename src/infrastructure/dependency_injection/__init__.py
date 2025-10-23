import logging

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from src.infrastructure import InfrastructureSettings
from .provider import InfrastructureProvider

log = logging.getLogger(__name__)


def setup_infrastructure_dependencies(
        app: FastAPI,
        settings: InfrastructureSettings,
) -> None:
    log.info('Initialize infrastructure dependencies')
    infrastructure_provider = InfrastructureProvider(settings)
    container = make_async_container(infrastructure_provider)

    setup_dishka(container=container, app=app)


__all__ = (
    "setup_infrastructure_dependencies",
)