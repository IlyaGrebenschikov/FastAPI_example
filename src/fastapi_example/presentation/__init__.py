import logging
from typing import Optional, Any

from fastapi import FastAPI

log = logging.getLogger(__name__)


def init_app(
    *sub_apps: tuple[str, FastAPI, Optional[str]],
    **kwargs: Any
) -> FastAPI:
    log.debug('Initialize General API')
    app = FastAPI(
        docs_url=None,
        redoc_url=None,
        swagger_ui_oauth2_redirect_url=None,
        **kwargs
    )

    for apps in sub_apps:
        app.mount(*apps)
        
    return app
