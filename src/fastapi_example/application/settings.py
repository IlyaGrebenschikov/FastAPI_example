import logging
from dataclasses import dataclass

log = logging.getLogger(__name__)


@dataclass
class ApplicationSettings: ...


def load_application_settings() -> ApplicationSettings:
    log.debug("Loading application settings.")
    return ApplicationSettings()
