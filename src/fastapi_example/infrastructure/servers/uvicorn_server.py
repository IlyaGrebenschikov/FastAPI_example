import logging

import uvicorn
from fastapi import FastAPI

from fastapi_example.infrastructure.settings import UvicornServerSettings

log = logging.getLogger(__name__)


async def run_uvicorn_server(
    app: FastAPI,
    settings: UvicornServerSettings,
) -> None:
    log.debug("Running Uvicorn server.")
    config = uvicorn.Config(app, **settings.model_dump())
    server = uvicorn.Server(config)
    await server.serve()
