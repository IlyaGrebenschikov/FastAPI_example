import logging
from typing import Any, Optional

from fastapi import FastAPI

from .controllers import (
    setup_controllers,
    )
from .handlers import setup_exception_handlers
from src.presentation.settings import AppSettings

log = logging.getLogger(__name__)


def init_app_v1(
    settings: AppSettings, 
    **kwargs: Any
    ) -> tuple[str, FastAPI, Optional[str]]:
    log.info("Initialize V1 API")
    app = FastAPI(
        **settings.app.model_dump(),
        **kwargs
        )

    setup_controllers(
        app,
    )
    setup_exception_handlers(app)

    return ("/api/v1", app, None)
