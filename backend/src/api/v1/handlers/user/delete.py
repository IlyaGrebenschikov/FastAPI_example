from typing import Annotated

from fastapi import Depends

from backend.src.utils.providers.stub import Stub
from backend.src.common.dto.user import UserResponseSchema, UserInDBSchema
from backend.src.cache.core.client import RedisClient
from backend.src.services.gateway import ServiceGateway


class DeleteUserHandler:
    def __init__(
            self,
            gateway: Annotated[ServiceGateway, Depends(Stub(ServiceGateway))],
            cache: Annotated[RedisClient, Depends(Stub(RedisClient))]
    ) -> None:
        self._gateway = gateway
        self._cache = cache

    async def execute(self, current_user: UserInDBSchema) -> UserResponseSchema:
        async with self._gateway:
            await self._gateway.database.manager.create_transaction()

            return await self._gateway.user().delete(current_user.id, self._cache)
