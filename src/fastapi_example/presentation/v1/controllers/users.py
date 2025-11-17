from typing import Annotated

from fastapi import APIRouter, Security, status
from dishka.integrations.fastapi import DishkaRoute, FromDishka

from fastapi_example.application.dto import (
    CreateUserDTO,
    UserResponseDTO,
    UpdateUserDTO
)
from fastapi_example.presentation.v1.dependencies import get_bearer_token
from fastapi_example.presentation.v1.docs import ConflictError, NotFoundError
from fastapi_example.application.interfaces.services import IUsersService

users_router = APIRouter(
    prefix="/users",
    tags=["users"],
    route_class=DishkaRoute
)


@users_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponseDTO,
    responses={
        status.HTTP_409_CONFLICT: {'model': ConflictError},
    },
)
async def create_user(
        user: CreateUserDTO,
        service: FromDishka[IUsersService]
) -> UserResponseDTO:
    return await service.create_user(user)


@users_router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=UserResponseDTO,
    responses={
    status.HTTP_404_NOT_FOUND: {'model': NotFoundError},
}
)
async def get_user(
        token: Annotated[str, Security(get_bearer_token)],
        service: FromDishka[IUsersService]
) -> UserResponseDTO:
    return await service.get_user(token)


@users_router.patch(
    "",
    status_code=status.HTTP_200_OK,
    response_model=UserResponseDTO,
    responses={
        status.HTTP_409_CONFLICT: {'model': ConflictError},
        status.HTTP_404_NOT_FOUND: {'model': NotFoundError},
    }
)
async def update_user(
        token: Annotated[str, Security(get_bearer_token)],
        service: FromDishka[IUsersService],
        data: UpdateUserDTO
) -> UserResponseDTO:
    return await service.update_user(token, data)


@users_router.delete(
    "",
    status_code=status.HTTP_200_OK,
    response_model=UserResponseDTO,
    responses={
        status.HTTP_404_NOT_FOUND: {'model': NotFoundError},
    }
)
async def delete_user(
        token: Annotated[str, Security(get_bearer_token)],
        service: FromDishka[IUsersService]
) -> UserResponseDTO:
    return await service.delete_user(token)
