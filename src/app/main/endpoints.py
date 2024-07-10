from fastapi import FastAPI

from src.app.api.v1.endpoints.test import test_router


def init_routers(app: FastAPI) -> None:
    app.include_router(test_router, prefix="/api/v1/test")
