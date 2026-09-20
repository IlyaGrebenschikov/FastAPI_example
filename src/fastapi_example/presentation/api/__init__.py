from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from fastapi_example.core.configs import AppConfig, CorsConfig

from .controllers import setup_controllers
from .handlers import setup_cors_middleware, setup_exception_handlers


def init_api(
    app_config: AppConfig,
    cors_config: CorsConfig,
    di_container: AsyncContainer,
) -> FastAPI:
    app = FastAPI(**app_config.model_dump())
    setup_exception_handlers(app)
    setup_cors_middleware(app, cors_config)
    setup_controllers(app)
    setup_dishka(di_container, app)
    return app
