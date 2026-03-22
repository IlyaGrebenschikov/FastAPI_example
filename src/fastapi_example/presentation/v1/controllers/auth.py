from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from fastapi_example.application.dto import Token
from fastapi_example.application.interfaces.services import (
    IAuthService,
    LoginCredentials,
    IRateLimiterService
)
from fastapi_example.presentation.v1.docs import UnAuthorizedError

auth_router = APIRouter(
    prefix="/token",
    tags=["token"],
    route_class=DishkaRoute
)


@auth_router.post(
    "",
    response_model=Token,
    status_code=status.HTTP_201_CREATED, responses={
        status.HTTP_401_UNAUTHORIZED: {'model': UnAuthorizedError},
    })
async def token(
        request: Request,
        query: Annotated[OAuth2PasswordRequestForm, Depends()],
        auth_service: FromDishka[IAuthService],
        rate_limiter_service: Annotated[IRateLimiterService, FromDishka[IRateLimiterService]]
) -> Token:
    credentials = LoginCredentials(
        username=query.username,
        password=query.password,
        scopes=query.scopes,
    )
    await rate_limiter_service.check(f"ip:{request.client.host}", request.url.path, limit=100, window=60)
    return await auth_service.login(credentials)
