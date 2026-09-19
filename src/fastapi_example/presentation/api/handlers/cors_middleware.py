import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi_example.core.configs import CorsConfig

log = logging.getLogger(__name__)


def setup_cors_middleware(app: FastAPI, cors: CorsConfig) -> None:
    log.info("Setting up CORS middleware")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors.origins,
        allow_credentials=True,
        allow_methods=cors.methods,
        allow_headers=cors.headers,
    )
