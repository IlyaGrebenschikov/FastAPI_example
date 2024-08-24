from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from user_service.src.services.security.token_jwt import TokenJWT
from user_service.src.services.security.bcrypt_hasher import BcryptHasher
from user_service.src.database.gateway import DBGateway
from user_service.src.utils.providers.stub import Stub
from user_service.src.api.v1.handlers.auth.login import LoginHandler
from user_service.src.common.exceptions import IncorrectDataException, NotFoundException
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
        status.HTTP_404_NOT_FOUND: {'model': NotFoundError},
    }
)
async def token(
        query: Annotated[OAuth2PasswordRequestForm, Depends()],
        gateway: Annotated[DBGateway, Depends(Stub(DBGateway))],
        hasher: Annotated[BcryptHasher, Depends(Stub(BcryptHasher))],
        jwt: Annotated[TokenJWT, Depends(Stub(TokenJWT))]
) -> Token:
    login_handler = LoginHandler(gateway, hasher, jwt)

    try:
        return await login_handler.execute(query)

    except IncorrectDataException as incorrect:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, incorrect.get_dict(), {"WWW-Authenticate": "Bearer"})

    except NotFoundException as not_found:
        raise HTTPException(status.HTTP_404_NOT_FOUND, not_found.get_dict())
