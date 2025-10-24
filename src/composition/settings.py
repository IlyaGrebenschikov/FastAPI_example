import logging
from dataclasses import dataclass
from typing import Optional

from src.infrastructure import InfrastructureSettings, load_infrastructure_settings
from src.presentation.servers.settings import ServerSettings, load_server_settings
from src.presentation.v1 import V1APISettings, load_v1_api_settings

log = logging.getLogger(__name__)

@dataclass
class Settings:
    server_settings: ServerSettings
    v1_api_settings: V1APISettings
    infrastructure_settings: InfrastructureSettings


def load_settings(
        server_settings: Optional[ServerSettings] = None,
        v1_api_settings: Optional[V1APISettings] = None,
        infrastructure_settings: Optional[InfrastructureSettings] = None
) -> Settings:
    log.info("Loading core settings.")
    return Settings(
        server_settings=server_settings or load_server_settings(),
        v1_api_settings=v1_api_settings or load_v1_api_settings(),
        infrastructure_settings=infrastructure_settings or load_infrastructure_settings()
    )
