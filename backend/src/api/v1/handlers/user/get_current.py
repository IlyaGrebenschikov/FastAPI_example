from typing import Annotated
from datetime import timedelta

from fastapi import Depends

from backend.src.database.gateway import DBGateway
from backend.src.common.dto.user import UserInDBSchema
from backend.src.common.exceptions import NotFoundException
from backend.src.common.converters.database import from_model_to_dto
from backend.src.common.converters.cache import from_dict_to_dto
from backend.src.common.converters.user import convert_sending, convert_receiving
from backend.src.services.security.token_jwt import TokenJWT
from backend.src.utils.providers.stub import Stub
from backend.src.settings.dependencies import oauth2_scheme
from backend.src.cache.core.client import RedisClient


class GetCurrentUserHandler:
    def __init__(
            self,
            gateway: Annotated[DBGateway, Depends(Stub(DBGateway))],
            jwt: Annotated[TokenJWT, Depends(Stub(TokenJWT))],
            cache: Annotated[RedisClient, Depends(Stub(RedisClient))],
            token: Annotated[str, Depends(oauth2_scheme)]
    ) -> None:
        self._gateway = gateway
        self._jwt = jwt
        self._cache = cache
        self._token = token

    async def execute(self) -> UserInDBSchema:
        user_id = (self._jwt.verify_jwt_token(self._token)).get('sub')
        cached_data = await self._cache.get_dict_all(user_id)

        if cached_data:
            return from_dict_to_dto(convert_receiving(cached_data), UserInDBSchema)

        async with self._gateway:
            result = await self._gateway.user().get_one(user_id=user_id)

        if not result:
            raise NotFoundException('User not found')

        converted_result = from_model_to_dto(result, UserInDBSchema)

        await self._cache.set_dict(user_id, convert_sending(converted_result.model_dump()))
        # Todo Change it so that the timedelta is taken from .env.
        await self._cache.set_expire(user_id, timedelta(minutes=30))

        return converted_result
