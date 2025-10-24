import logging

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from src.infrastructure import InfrastructureSettings
from src.infrastructure.di_providers import DatabaseProvider

log = logging.getLogger(__name__)


def setup_dependencies(
        app: FastAPI,
        infra_settings: InfrastructureSettings,
) -> None:
    log.info('Initialize infrastructure dependencies')
    database_provider = DatabaseProvider(infra_settings)
    container = make_async_container(
        database_provider,
    )

    setup_dishka(container=container, app=app)
