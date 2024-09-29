from typing import Annotated

from fastapi import Depends

from backend.src.common.dto.user import UserInDBSchema
from backend.src.services.security.token_jwt import TokenJWT
from backend.src.utils.providers.stub import Stub
from backend.src.settings.dependencies import oauth2_scheme
from backend.src.cache.core.client import RedisClient
from backend.src.core.settings import RedisSettings
from backend.src.services.gateway import ServiceGateway


class GetCurrentUserHandler:
    def __init__(
            self,
            gateway: Annotated[ServiceGateway, Depends(Stub(ServiceGateway))],
            jwt: Annotated[TokenJWT, Depends(Stub(TokenJWT))],
            cache: Annotated[RedisClient, Depends(Stub(RedisClient))],
            cache_settings: Annotated[RedisSettings, Depends(Stub(RedisSettings))],
            token: Annotated[str, Depends(oauth2_scheme)]
    ) -> None:
        self._gateway = gateway
        self._jwt = jwt
        self._cache = cache
        self._cache_settings = cache_settings
        self._token = token

    async def execute(self) -> UserInDBSchema:
        user_id = (self._jwt.verify_jwt_token(self._token)).get('sub')

        async with self._gateway:
            result = await self._gateway.user().get(user_id, self._cache_settings.USER_TTL, self._cache)

        return result
