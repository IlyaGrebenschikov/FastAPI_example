from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from fastapi_example.application.dto import Token, LoginCredentials
from fastapi_example.application.interfaces.services import (
    IAuthService,
    IRateLimiterService,
)
from fastapi_example.presentation.api.common.docs import (
    TooManyRequestsError,
    UnAuthorizedError,
)

auth_router = APIRouter(prefix="/api/v1/token", tags=["token"], route_class=DishkaRoute)


@auth_router.post(
    "",
    response_model=Token,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": UnAuthorizedError},
        status.HTTP_429_TOO_MANY_REQUESTS: {"model": TooManyRequestsError},
    },
)
async def token(
    request: Request,
    query: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: FromDishka[IAuthService],
    rate_limiter_service: FromDishka[IRateLimiterService],
) -> Token:
    credentials = LoginCredentials(
        username=query.username,
        password=query.password,
        scopes=query.scopes,
    )
    await rate_limiter_service.check(
        f"ip:{request.client.host}", request.url.path, limit=100, window=60
    )
    return await auth_service.login(credentials)
