from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from user_service.src.api.v1.handlers.auth.login import LoginHandler
from user_service.src.common.exceptions import NotFoundException, UnAuthorizedException
from user_service.src.common.dto.token import Token
from user_service.src.common.dto.docs import BadRequestError, NotFoundError


auth_router = APIRouter(tags=['auth'])


@auth_router.post(
    '/token',
    status_code=status.HTTP_200_OK,
    response_model=Token,
    response_description='JWT token resource',
    description='Retrieves a JWT token resource',
    summary='Retrieves a JWT token resource',
    responses={
        status.HTTP_400_BAD_REQUEST: {'model': BadRequestError},
        status.HTTP_401_UNAUTHORIZED: {'model': NotFoundError},
    }
)
async def token(
        query: Annotated[OAuth2PasswordRequestForm, Depends()],
        handler: Annotated[LoginHandler, Depends(LoginHandler)]
) -> Token:
    try:
        return await handler.execute(query)

    except UnAuthorizedException as un_auth_error:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, un_auth_error.get_dict(), {"WWW-Authenticate": "Bearer"})

    except NotFoundException as not_found:
        raise HTTPException(status.HTTP_404_NOT_FOUND, not_found.get_dict())