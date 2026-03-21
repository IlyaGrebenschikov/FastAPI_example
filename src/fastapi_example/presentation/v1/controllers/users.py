from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Security, status

from fastapi_example.application.dto import (
    CreateUserDTO,
    DeleteUserDTO,
    UpdateUserDTO,
    UserResponseDTO,
)
from fastapi_example.application.interfaces.services import (
    ITokenJWTService,
    IUsersService,
)
from fastapi_example.presentation.v1.dependencies import get_bearer_token
from fastapi_example.presentation.v1.docs import (
    ConflictError,
    ForbiddenError,
    NotFoundError,
    UnAuthorizedError,
)

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
        data: CreateUserDTO,
        user_service: Annotated[IUsersService, FromDishka[IUsersService]],
) -> UserResponseDTO:
    return await user_service.create_user(data)


@users_router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=UserResponseDTO,
    responses={
        status.HTTP_401_UNAUTHORIZED: {'model': UnAuthorizedError},
        status.HTTP_404_NOT_FOUND: {'model': NotFoundError},
    }
)
async def get_user(
        token: Annotated[str, Security(get_bearer_token)],
        user_service: Annotated[IUsersService, FromDishka[IUsersService]],
        jwt_service: Annotated[ITokenJWTService, FromDishka[ITokenJWTService]]
) -> UserResponseDTO:
    user_id = jwt_service.get_user_id_from_token(token)
    return await user_service.get_user(user_id)


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
        data: UpdateUserDTO,
        user_service: Annotated[IUsersService, FromDishka[IUsersService]],
        jwt_service: Annotated[ITokenJWTService, FromDishka[ITokenJWTService]]
) -> UserResponseDTO:
    user_id = jwt_service.get_user_id_from_token(token)
    return await user_service.update_user(user_id, data)


@users_router.delete(
    "",
    status_code=status.HTTP_200_OK,
    response_model=UserResponseDTO,
    responses={
        status.HTTP_404_NOT_FOUND: {'model': NotFoundError},
        status.HTTP_403_FORBIDDEN: {'model': ForbiddenError},
    }
)
async def delete_user(
        token: Annotated[str, Security(get_bearer_token)],
        data: DeleteUserDTO,
        user_service: Annotated[IUsersService, FromDishka[IUsersService]],
        jwt_service: Annotated[ITokenJWTService, FromDishka[ITokenJWTService]]
) -> UserResponseDTO:
    user_id = jwt_service.get_user_id_from_token(token)
    return await user_service.delete_user(user_id, data)
