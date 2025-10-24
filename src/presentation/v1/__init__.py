import logging
from typing import Any, Optional

from fastapi import FastAPI

from .controllers import (
    setup_controllers,
    )
from .handlers import setup_exception_handlers
from .middlewares import setup_middlewares
from .settings import V1APISettings, load_v1_api_settings

log = logging.getLogger(__name__)


def init_app_v1(
    settings: V1APISettings, 
    **kwargs: Any
    ) -> tuple[str, FastAPI, Optional[str]]:
    log.info("Initialize V1 API")
    app = FastAPI(
        **settings.app.model_dump(),
        **kwargs
        )

    setup_controllers()
    setup_exception_handlers()
    setup_middlewares()

    return ("/api/v1", app, None)


__all__ = (
    "V1APISettings",
    "init_app_v1",
    "load_v1_api_settings"
)
