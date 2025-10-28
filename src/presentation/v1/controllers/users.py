from fastapi import (
    APIRouter,
    status
)
from dishka.integrations.fastapi import (
    DishkaRoute,
    FromDishka
)

from src.application.dto import (
    CreateUserDTO,
    UserResponseDTO
)
from src.presentation.v1.docs import ConflictError
from src.application.interfaces.services import IUsersService

users_router = APIRouter(prefix="/users", tags=["users"], route_class=DishkaRoute)


@users_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponseDTO,
    responses={
        status.HTTP_409_CONFLICT: {'model': ConflictError},
    },
)
async def create_user(user: CreateUserDTO, service: FromDishka[IUsersService]) -> UserResponseDTO:
    return await service.create_user(user)
