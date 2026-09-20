import logging

import uvicorn
from fastapi import FastAPI

from fastapi_example.core.settings import ServerSettings

log = logging.getLogger(__name__)


async def run_uvicorn_server(
    app: FastAPI,
    settings: ServerSettings,
) -> None:
    log.debug("Running Uvicorn server.")
    config = uvicorn.Config(app, **settings.model_dump())
    server = uvicorn.Server(config)
    await server.serve()
