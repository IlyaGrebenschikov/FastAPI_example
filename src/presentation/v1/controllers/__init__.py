from fastapi import FastAPI, APIRouter

from .users import users_router

def setup_controllers(app: FastAPI, *routers: APIRouter) -> None:
    v1_router = APIRouter()

    for router in routers:
        v1_router.include_router(router)

    app.include_router(v1_router)


__all__ = (
    "setup_controllers",
    "users_router"
)
