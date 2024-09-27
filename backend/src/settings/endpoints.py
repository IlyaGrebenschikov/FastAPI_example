import logging

from fastapi import FastAPI

from backend.src.api.v1.endpoints.healthcheck import healthcheck_router
from backend.src.api.v1.endpoints.user import user_router
from backend.src.api.v1.endpoints.auth import auth_router
from backend.src.core.logger import setup_logger, setup_logger_file_handler, setup_logger_stream_handler


logger_file_handler = setup_logger_file_handler(logging.DEBUG, 'app')
logger_stream_handler = setup_logger_stream_handler(logging.DEBUG)
logger = setup_logger(__name__, logging.DEBUG, logger_file_handler, logger_stream_handler)


def init_routers(app: FastAPI) -> None:
    logger.debug('Initialize API endpoints')
    app.include_router(healthcheck_router, prefix="/api/v1/healthcheck")
    app.include_router(user_router, prefix="/api/v1/user")
    app.include_router(auth_router, prefix="/api/v1/token")
