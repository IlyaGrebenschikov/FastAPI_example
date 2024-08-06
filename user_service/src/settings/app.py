from typing import Optional

import uvicorn
from fastapi import FastAPI

from user_service.src.settings.endpoints import init_routers
from user_service.src.settings.dependencies import init_dependencies
from user_service.src.core.settings import DatabaseSettings, JWTSettings


def init_app(
        db_settings: DatabaseSettings,
        jwt_settings: JWTSettings,
        title: str = 'FastAPI',
        docs_url: Optional[str] = "/docs",
        redoc_url: Optional[str] = "/redoc",
) -> FastAPI:
    app = FastAPI(
        title=title,
        docs_url=docs_url,
        redoc_url=redoc_url,
    )
    init_routers(app)
    init_dependencies(app, db_settings, jwt_settings)

    return app


def start_app(app: FastAPI, host: str = '0.0.0.0', port: int = 8080) -> None:
    uvicorn.run(app, host=host, port=port)
