from typing import Annotated

from fastapi import Depends

from user_service.src.services.security.bcrypt_hasher import BcryptHasher
from user_service.src.database.gateway import DBGateway
from user_service.src.common.dto.user import UserInDBSchema
from user_service.src.common.exceptions import NotFoundException
from user_service.src.common.converters.database import from_model_to_dto
from user_service.src.services.security.token_jwt import TokenJWT
from user_service.src.utils.providers.stub import Stub
from user_service.src.settings.dependencies import oauth2_scheme


class GetCurrentUserHandler:
    def __init__(
            self,
            gateway: Annotated[DBGateway, Depends(Stub(DBGateway))],
            hasher: Annotated[BcryptHasher, Depends(Stub(BcryptHasher))],
            jwt: Annotated[TokenJWT, Depends(Stub(TokenJWT))],
            token: Annotated[int, Depends(oauth2_scheme)]
    ) -> None:
        self._gateway = gateway
        self._hasher = hasher
        self._jwt = jwt
        self._token = token

    async def execute(self):
        user_id = (self._jwt.verify_jwt_token(self._token)).get('sub')

        async with self._gateway:
            result = await self._gateway.user().get_one(user_id=user_id)

        if not result:
            raise NotFoundException('User not found')

        return from_model_to_dto(result, UserInDBSchema)
