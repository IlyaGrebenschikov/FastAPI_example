from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, status

from fastapi_example.application.features.users.commands import (
    CreateUserCommand,
    CreateUserHandler,
    DeleteUserCommand,
    DeleteUserHandler,
    UpdateUserCommand,
    UpdateUserHandler,
)
from fastapi_example.application.features.users.queries import (
    GetUserHandler,
    GetUserQuery,
)
from fastapi_example.presentation.api.dependencies import (
    RateLimitDep,
    get_current_user_id_from_access_token,
)
from fastapi_example.presentation.api.docs import (
    ConflictDoc,
    ForbiddenDoc,
    NotFoundDoc,
    TooManyRequestsDoc,
    UnauthorizedDoc,
)
from fastapi_example.presentation.api.dto import (
    CreateUserDTO,
    DeleteUserDTO,
    DeleteUserResponseDTO,
    UpdateUserDTO,
    UserResponseDTO,
)

users_router = APIRouter(prefix="/users", tags=["users"], route_class=DishkaRoute)


@users_router.post(
    "",
    response_model=UserResponseDTO,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {"model": ConflictDoc},
        status.HTTP_429_TOO_MANY_REQUESTS: {"model": TooManyRequestsDoc},
    },
)
async def create_user(
    data: CreateUserDTO,
    handler: FromDishka[CreateUserHandler],
    _rate_limit: RateLimitDep,
) -> UserResponseDTO:
    cmd = CreateUserCommand(email=data.email, password=data.password)
    user = await handler.execute(cmd)
    return UserResponseDTO.model_validate(user)


@users_router.get(
    "",
    response_model=UserResponseDTO,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": UnauthorizedDoc},
        status.HTTP_404_NOT_FOUND: {"model": NotFoundDoc},
        status.HTTP_429_TOO_MANY_REQUESTS: {"model": TooManyRequestsDoc},
    },
)
async def get_user(
    handler: FromDishka[GetUserHandler],
    user_id: UUID = Depends(get_current_user_id_from_access_token),  # noqa: B008
) -> UserResponseDTO:
    query = GetUserQuery(user_id=user_id)
    user = await handler.execute(query)
    return UserResponseDTO.model_validate(user)


@users_router.patch(
    "",
    response_model=UserResponseDTO,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": UnauthorizedDoc},
        status.HTTP_404_NOT_FOUND: {"model": NotFoundDoc},
        status.HTTP_409_CONFLICT: {"model": ConflictDoc},
        status.HTTP_429_TOO_MANY_REQUESTS: {"model": TooManyRequestsDoc},
    },
)
async def update_user(
    data: UpdateUserDTO,
    handler: FromDishka[UpdateUserHandler],
    user_id: UUID = Depends(get_current_user_id_from_access_token),  # noqa: B008
) -> UserResponseDTO:
    cmd = UpdateUserCommand(user_id=user_id, email=data.email, password=data.password)
    user = await handler.execute(cmd)
    return UserResponseDTO.model_validate(user)


@users_router.delete(
    "",
    response_model=DeleteUserResponseDTO,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": UnauthorizedDoc},
        status.HTTP_403_FORBIDDEN: {"model": ForbiddenDoc},
        status.HTTP_404_NOT_FOUND: {"model": NotFoundDoc},
        status.HTTP_429_TOO_MANY_REQUESTS: {"model": TooManyRequestsDoc},
    },
)
async def delete_user(
    data: DeleteUserDTO,
    handler: FromDishka[DeleteUserHandler],
    user_id: UUID = Depends(get_current_user_id_from_access_token),  # noqa: B008
) -> DeleteUserResponseDTO:
    cmd = DeleteUserCommand(user_id=user_id, password=data.password)
    await handler.execute(cmd)
    return DeleteUserResponseDTO()
