import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.presentation.v1.settings import CORSSettings

log = logging.getLogger(__name__)


def setup_cors_middleware(app: FastAPI, settings: CORSSettings) -> None:
    log.info("Setting up CORS middleware")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.origins,
        allow_credentials=True,
        allow_methods=settings.methods,
        allow_headers=settings.headers,
    )
