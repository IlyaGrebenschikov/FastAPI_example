from typing import Annotated

from dishka.integrations.fastapi import (
    DishkaRoute,
    FromDishka
)
from fastapi import (
    APIRouter,
    status, Depends
)
from fastapi.security import OAuth2PasswordRequestForm

from src.application.dto import Token
from src.application.interfaces.services import IAuthService
from src.presentation.v1.docs import NotFoundError

auth_router = APIRouter(prefix="/token", tags=["token"], route_class=DishkaRoute)

@auth_router.post(
    "",
    response_model=Token,
    status_code=status.HTTP_201_CREATED, responses={
        status.HTTP_401_UNAUTHORIZED: {'model': NotFoundError},
    })
async def token(
        query: Annotated[OAuth2PasswordRequestForm, Depends()],
        auth_service: FromDishka[IAuthService]
) -> Token:
    return await auth_service.login(query)
