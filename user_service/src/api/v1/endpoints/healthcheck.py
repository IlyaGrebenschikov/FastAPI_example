from fastapi import APIRouter, status

from user_service.src.common.dto.healthcheck import HealthCheckResponseSchema


healthcheck_router = APIRouter(tags=["healthcheck"])


@healthcheck_router .get(
    "/healthcheck",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheckResponseSchema
)
async def healthcheck_endpoint() -> dict[str, bool]:
    return {
        'healthy': True
    }
