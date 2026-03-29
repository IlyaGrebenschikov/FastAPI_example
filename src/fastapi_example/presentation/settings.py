import logging
from dataclasses import dataclass
from typing import Optional

from .api.v1 import V1APISettings, load_v1_api_settings

log = logging.getLogger(__name__)


@dataclass
class PresentationSettings:
    v1_api: V1APISettings


def load_presentation_settings(
    v1_api_settings: Optional[V1APISettings] = None,
) -> PresentationSettings:
    log.debug("Loading presentation settings.")
    return PresentationSettings(v1_api=v1_api_settings or load_v1_api_settings())
