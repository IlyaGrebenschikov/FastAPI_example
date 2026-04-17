import logging
from dataclasses import dataclass

from fastapi_example.infrastructure import AppSettings, CORSSettings

log = logging.getLogger(__name__)


@dataclass
class V1APISettings:
    app: AppSettings
    cors: CORSSettings


@dataclass
class ApplicationSettings:
    v1_api: V1APISettings


def load_application_settings(
    app_settings: AppSettings, cors_settings: CORSSettings
) -> ApplicationSettings:
    log.debug("Loading application settings.")
    v1_api = V1APISettings(app=app_settings, cors=cors_settings)
    return ApplicationSettings(v1_api)
