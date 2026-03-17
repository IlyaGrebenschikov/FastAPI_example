import logging

import uvicorn
from fastapi import FastAPI

from fastapi_example.infrastructure.settings import UvicornServerSettings

log = logging.getLogger(__name__)


def run_uvicorn_server(
        app: FastAPI,
        settings: UvicornServerSettings,
) -> None:
    log.debug("Running Uvicorn server.")
    uvicorn.run(app, **settings.model_dump())
