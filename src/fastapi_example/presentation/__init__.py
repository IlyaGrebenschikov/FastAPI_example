import logging
from typing import Any, Optional

from fastapi import FastAPI

from .settings import PresentationSettings, load_presentation_settings

log = logging.getLogger(__name__)


def init_app(
    *sub_apps: tuple[str, FastAPI, Optional[str]],
    **kwargs: Any
) -> FastAPI:
    log.debug("Initialize General API")
    app = FastAPI(
        docs_url=None,
        redoc_url=None,
        swagger_ui_oauth2_redirect_url=None,
        **kwargs
    )

    for apps in sub_apps:
        app.mount(*apps)

    return app


__all__ = (
    "PresentationSettings",
    "load_presentation_settings",
    "init_app",
)
