from fastapi import APIRouter, status

health_router = APIRouter(tags=["health"])


@health_router.get(
    "/health",
    status_code=status.HTTP_200_OK,
)
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
