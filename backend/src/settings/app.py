import logging
from typing import Optional

import uvicorn
from fastapi import FastAPI

from backend.src.settings.endpoints import init_routers
from backend.src.settings.dependencies import init_dependencies
from backend.src.core.settings import DatabaseSettings, JWTSettings, RedisSettings, get_logger_settings
from backend.src.core.logger import setup_logger, setup_logger_file_handler, setup_logger_stream_handler


logger_settings = get_logger_settings()
logger_file_handler = setup_logger_file_handler(logger_settings, logging.INFO, 'app')
logger_stream_handler = setup_logger_stream_handler(logger_settings, logging.INFO)
logger = setup_logger(__name__, logging.INFO, logger_file_handler, logger_stream_handler)


def init_app(
        db_settings: DatabaseSettings,
        jwt_settings: JWTSettings,
        redis_settings: RedisSettings,
        title: str = 'FastAPI',
        docs_url: Optional[str] = "/docs",
        redoc_url: Optional[str] = "/redoc",
) -> FastAPI:
    logger.debug('Initialize API')
    app = FastAPI(
        title=title,
        docs_url=docs_url,
        redoc_url=redoc_url,
    )
    init_routers(app)
    init_dependencies(app, db_settings, jwt_settings, redis_settings)

    return app


def start_app(app: FastAPI, host: str = '0.0.0.0', port: int = 8080) -> None:
    logger.info('Running API')
    uvicorn.run(app, host=host, port=port)
