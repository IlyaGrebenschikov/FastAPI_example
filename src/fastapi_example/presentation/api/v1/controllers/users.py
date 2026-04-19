from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Request, Security, status

from fastapi_example.presentation.api.v1.dto import CreateUserDTO, UserResponseDTO, UpdateUserDTO, DeleteUserDTO
from fastapi_example.application.interfaces.services import (
    IRateLimiterService,
    ITokenJWTService,
)
from fastapi_example.application.features.users.create_user import CreateUserCommand, CreateUserHandler
from fastapi_example.application.features.users.get_user import GetUserQuery, GetUserHandler
from fastapi_example.application.features.users.update_user import UpdateUserCommand, UpdateUserHandler
from fastapi_example.application.features.users.delete_user import DeleteUserCommand, DeleteUserHandler
from fastapi_example.presentation.api.v1.dependencies import get_bearer_token
from fastapi_example.presentation.api.common.docs import (
    ConflictError,
    ForbiddenError,
    NotFoundError,
    TooManyRequestsError,
    UnAuthorizedError,
)

users_router = APIRouter(
    prefix="/api/v1/users", tags=["users"], route_class=DishkaRoute
)


@users_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponseDTO,
    responses={
        status.HTTP_409_CONFLICT: {"model": ConflictError},
        status.HTTP_429_TOO_MANY_REQUESTS: {"model": TooManyRequestsError},
    },
)
async def create_user(
    request: Request,
    data: CreateUserDTO,
    handler: FromDishka[CreateUserHandler],
    rate_limiter_service: FromDishka[IRateLimiterService],
) -> UserResponseDTO:
    await rate_limiter_service.check(
        f"ip:{request.client.host}", request.url.path, limit=100, window=60
    )
    cmd = CreateUserCommand(username=data.username, email=data.email, password=data.password)
    user = await handler.execute(cmd)
    return UserResponseDTO.model_validate(user, from_attributes=True)


@users_router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=UserResponseDTO,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": UnAuthorizedError},
        status.HTTP_404_NOT_FOUND: {"model": NotFoundError},
        status.HTTP_429_TOO_MANY_REQUESTS: {"model": TooManyRequestsError},
    },
)
async def get_user(
    request: Request,
    token: Annotated[str, Security(get_bearer_token)],
    handler: FromDishka[GetUserHandler],
    jwt_service: FromDishka[ITokenJWTService],
    rate_limiter_service: FromDishka[IRateLimiterService],
) -> UserResponseDTO:
    await rate_limiter_service.check(
        f"ip:{request.client.host}", request.url.path, limit=100, window=60
    )
    user_id = jwt_service.get_user_id_from_token(token)
    await rate_limiter_service.check(
        f"user:{user_id}", request.url.path, limit=20, window=60
    )
    query = GetUserQuery(user_id)
    user = await handler.execute(query)
    return UserResponseDTO.model_validate(user, from_attributes=True)


@users_router.patch(
    "",
    status_code=status.HTTP_200_OK,
    response_model=UserResponseDTO,
    responses={
        status.HTTP_409_CONFLICT: {"model": ConflictError},
        status.HTTP_404_NOT_FOUND: {"model": NotFoundError},
        status.HTTP_429_TOO_MANY_REQUESTS: {"model": TooManyRequestsError},
    },
)
async def update_user(
    request: Request,
    token: Annotated[str, Security(get_bearer_token)],
    data: UpdateUserDTO,
    handler: FromDishka[UpdateUserHandler],
    jwt_service: FromDishka[ITokenJWTService],
    rate_limiter_service: FromDishka[IRateLimiterService],
) -> UserResponseDTO:
    await rate_limiter_service.check(
        f"ip:{request.client.host}", request.url.path, limit=100, window=60
    )
    user_id = jwt_service.get_user_id_from_token(token)
    await rate_limiter_service.check(
        f"user:{user_id}", request.url.path, limit=20, window=60
    )
    cmd = UpdateUserCommand(user_id, data.username, data.email)
    return UserResponseDTO.model_validate(await handler.execute(cmd), from_attributes=True)


@users_router.delete(
    "",
    status_code=status.HTTP_200_OK,
    response_model=UserResponseDTO,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": NotFoundError},
        status.HTTP_403_FORBIDDEN: {"model": ForbiddenError},
        status.HTTP_429_TOO_MANY_REQUESTS: {"model": TooManyRequestsError},
    },
)
async def delete_user(
    request: Request,
    token: Annotated[str, Security(get_bearer_token)],
    data: DeleteUserDTO,
    handler: FromDishka[DeleteUserHandler],
    jwt_service: FromDishka[ITokenJWTService],
    rate_limiter_service: FromDishka[IRateLimiterService],
) -> UserResponseDTO:
    await rate_limiter_service.check(
        f"ip:{request.client.host}", request.url.path, limit=100, window=60
    )
    user_id = jwt_service.get_user_id_from_token(token)
    await rate_limiter_service.check(
        f"user:{user_id}", request.url.path, limit=20, window=60
    )
    cmd = DeleteUserCommand(user_id, data.password)
    return UserResponseDTO.model_validate(await handler.execute(cmd), from_attributes=True)
