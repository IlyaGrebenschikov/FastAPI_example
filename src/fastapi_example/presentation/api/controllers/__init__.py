from fastapi import FastAPI

from .auth import auth_router
from .health import health_router
from .users import users_router


def setup_controllers(app: FastAPI) -> None:
    app.include_router(health_router)
    app.include_router(auth_router)
    app.include_router(users_router)


__all__ = ("setup_controllers",)
