import logging
from dataclasses import dataclass
from typing import Optional

from fastapi_example.application import ApplicationSettings, load_application_settings
from fastapi_example.infrastructure import InfrastructureSettings, load_infrastructure_settings
from fastapi_example.presentation import PresentationSettings, load_presentation_settings

log = logging.getLogger(__name__)


@dataclass
class Settings:
    presentation: PresentationSettings
    infrastructure: InfrastructureSettings
    application: ApplicationSettings


def load_settings(
        presentation_settings: Optional[PresentationSettings] = None,
        infrastructure_settings: Optional[InfrastructureSettings] = None,
        application_settings: Optional[ApplicationSettings] = None,
) -> Settings:
    log.debug("Loading core settings.")
    return Settings(
        presentation=presentation_settings or load_presentation_settings(),
        infrastructure=infrastructure_settings or load_infrastructure_settings(),
        application=application_settings or load_application_settings(),
    )
