from fastapi import APIRouter
from dishka.integrations.fastapi import DishkaRoute, FromDishka

from src.application.dto import CreateUserDTO, UserResponseDTO
from src.application.interfaces.services import IUsersService

users_router = APIRouter(prefix="/users", tags=["users"], route_class=DishkaRoute)


@users_router.post("", response_model=UserResponseDTO)
async def create_user(user: CreateUserDTO, service: FromDishka[IUsersService]) -> UserResponseDTO:
    return await service.create_user(user)
