import logging

from fastapi import FastAPI

from fastapi_example.application.settings import V1APISettings
from fastapi_example.presentation.api.common.middlewares import setup_cors_middleware

log = logging.getLogger(__name__)


def setup_middlewares(app: FastAPI, settings: V1APISettings) -> None:
    log.debug("Setting up middlewares")
    setup_cors_middleware(app, settings.cors)
