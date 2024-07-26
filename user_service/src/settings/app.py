from fastapi import FastAPI

from user_service.src.settings.endpoints import init_routers


def create_app() -> FastAPI:
    app = FastAPI()
    init_routers(app)

    return app
