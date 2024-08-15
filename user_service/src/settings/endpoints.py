from fastapi import FastAPI

from user_service.src.api.v1.endpoints.healthcheck import healthcheck_router


def init_routers(app: FastAPI) -> None:
    app.include_router(healthcheck_router, prefix="/api/v1/healthcheck")
