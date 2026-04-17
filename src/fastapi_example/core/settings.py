import logging
from dataclasses import dataclass
from typing import Optional

from fastapi_example.application import ApplicationSettings, load_application_settings
from fastapi_example.infrastructure import (
    InfrastructureSettings,
    load_infrastructure_settings,
)

log = logging.getLogger(__name__)


@dataclass
class Settings:
    infrastructure: InfrastructureSettings
    application: ApplicationSettings


def load_settings(
    infrastructure_settings: Optional[InfrastructureSettings] = None,
    application_settings: Optional[ApplicationSettings] = None,
) -> Settings:
    log.debug("Loading core settings.")
    infra = infrastructure_settings or load_infrastructure_settings()
    app = application_settings or load_application_settings(infra.app, infra.cors)
    return Settings(
        infrastructure=infra,
        application=app,
    )
