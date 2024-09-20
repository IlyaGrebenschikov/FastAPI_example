from typing import Annotated
from datetime import timedelta

from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from backend.src.utils.providers.stub import Stub
from backend.src.database.gateway import DBGateway
from backend.src.common.dto.user import UpdateUserQuerySchema, UserResponseSchema, UserInDBSchema
from backend.src.services.security.bcrypt_hasher import BcryptHasher
from backend.src.cache.core.client import RedisClient
from backend.src.common.converters.database import from_model_to_dto
from backend.src.common.converters.user import none_filter
from backend.src.common.exceptions import ConflictException
from backend.src.common.converters.user import convert_sending


class UpdateUserHandler:
    def __init__(
            self,
            gateway: Annotated[DBGateway, Depends(Stub(DBGateway))],
            hasher: Annotated[BcryptHasher, Depends(Stub(BcryptHasher))],
            cache: Annotated[RedisClient, Depends(Stub(RedisClient))],
    ) -> None:
        self._gateway = gateway
        self._hasher = hasher
        self._cache = cache

    async def execute(self, current_user: UserInDBSchema, query: UpdateUserQuerySchema) -> UserResponseSchema:
        filtered_data = none_filter(query)

        if filtered_data.get('password'):
            filtered_data['password'] = self._hasher.hash_password(filtered_data['password'])

        async with self._gateway:
            try:
                await self._gateway.manager.create_transaction()
                result = await self._gateway.user().update(current_user.id, **filtered_data)

                await self._cache.set_dict(
                    current_user.id,
                    convert_sending(from_model_to_dto(result, UserInDBSchema).model_dump())
                )
                # Todo Change it so that the timedelta is taken from .env.
                await self._cache.set_expire(current_user.id, timedelta(minutes=30))

                return from_model_to_dto(result, UserResponseSchema)

            except IntegrityError:
                raise ConflictException('A user with this data already exists')
