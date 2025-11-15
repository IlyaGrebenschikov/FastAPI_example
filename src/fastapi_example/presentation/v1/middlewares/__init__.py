import logging

from fastapi import FastAPI

from .cors import setup_cors_middleware
from fastapi_example.presentation.v1.settings import V1APISettings

log = logging.getLogger(__name__)


def setup_middlewares(app: FastAPI, settings: V1APISettings) -> None:
    log.debug("Setting up middlewares")
    setup_cors_middleware(app, settings.cors)


__all__ = (
    "setup_middlewares",
)
