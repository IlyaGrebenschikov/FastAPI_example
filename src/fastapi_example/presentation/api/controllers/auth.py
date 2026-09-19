from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, status

from fastapi_example.application.features.auth.commands import (
    LoginEmailCommand,
    LoginEmailHandler,
    LogoutCommand,
    LogoutHandler,
    RefreshCommand,
    RefreshHandler,
)
from fastapi_example.application.interfaces.services import TokenData
from fastapi_example.presentation.api.dependencies import get_refresh_token_data
from fastapi_example.presentation.api.docs import (
    ConflictError,
    NotFoundError,
    TooManyRequestsError,
    UnAuthorizedError,
)
from fastapi_example.presentation.api.dto import (
    LoginEmailDTO,
    LogoutResponseDTO,
    TokenResponseDTO,
)

auth_router = APIRouter(prefix="/auth", tags=["auth"], route_class=DishkaRoute)


@auth_router.post(
    "/login/email",
    response_model=TokenResponseDTO,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": UnAuthorizedError},
        status.HTTP_429_TOO_MANY_REQUESTS: {"model": TooManyRequestsError},
    },
)
async def login_email(
    data: LoginEmailDTO,
    handler: FromDishka[LoginEmailHandler],
) -> TokenResponseDTO:
    cmd = LoginEmailCommand(email=data.email, password=data.password)
    pair = await handler.execute(cmd)
    return TokenResponseDTO(
        access_token=pair.access_token, refresh_token=pair.refresh_token
    )


@auth_router.post(
    "/refresh",
    response_model=TokenResponseDTO,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": UnAuthorizedError},
    },
)
async def refresh(
    handler: FromDishka[RefreshHandler],
    token_data: Annotated[TokenData, Depends(get_refresh_token_data)],
) -> TokenResponseDTO:
    cmd = RefreshCommand(user_id=token_data.user_id, jti=token_data.jti)
    pair = await handler.execute(cmd)
    return TokenResponseDTO(
        access_token=pair.access_token, refresh_token=pair.refresh_token
    )


@auth_router.post(
    "/logout",
    response_model=LogoutResponseDTO,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": UnAuthorizedError},
    },
)
async def logout(
    handler: FromDishka[LogoutHandler],
    token_data: Annotated[TokenData, Depends(get_refresh_token_data)],
) -> LogoutResponseDTO:
    cmd = LogoutCommand(user_id=token_data.user_id, jti=token_data.jti)
    await handler.execute(cmd)
    return LogoutResponseDTO()
