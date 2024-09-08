from fastapi import FastAPI

from backend.src.api.v1.endpoints.healthcheck import healthcheck_router
from backend.src.api.v1.endpoints.user import user_router
from backend.src.api.v1.endpoints.auth import auth_router


def init_routers(app: FastAPI) -> None:
    app.include_router(healthcheck_router, prefix="/api/v1/healthcheck")
    app.include_router(user_router, prefix="/api/v1/user")
    app.include_router(auth_router, prefix="/api/v1/token")
