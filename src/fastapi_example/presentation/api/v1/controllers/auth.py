from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from fastapi_example.presentation.api.v1.dto import TokenDTO
from fastapi_example.application.interfaces.services import (
    IRateLimiterService,
)
from fastapi_example.application.features.auth.create_access_token import (
    CreateAccessTokenHandler,
    CreateAccessTokenCommand,
)
from fastapi_example.presentation.api.common.docs import (
    TooManyRequestsError,
    UnAuthorizedError,
)

auth_router = APIRouter(prefix="/api/v1/token", tags=["token"], route_class=DishkaRoute)


@auth_router.post(
    "/access",
    response_model=TokenDTO,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": UnAuthorizedError},
        status.HTTP_429_TOO_MANY_REQUESTS: {"model": TooManyRequestsError},
    },
)
async def token(
    request: Request,
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    handler: FromDishka[CreateAccessTokenHandler],
    rate_limiter_service: FromDishka[IRateLimiterService],
) -> TokenDTO:
    cmd = CreateAccessTokenCommand(
        username=form.username,
        password=form.password,
        scopes=form.scopes,
    )
    await rate_limiter_service.check(
        f"ip:{request.client.host}", # type: ignore[union-attr]
        request.url.path,
        limit=100,
        window=60,
    )
    return TokenDTO(access_token=await handler.execute(cmd), token_type="Bearer")
