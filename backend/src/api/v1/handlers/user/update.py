import logging
from typing import Annotated

from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from backend.src.utils.providers.stub import Stub
from backend.src.common.dto.user import UpdateUserQuerySchema, UserResponseSchema, UserInDBSchema
from backend.src.services.security.bcrypt_hasher import BcryptHasher
from backend.src.cache.core.client import RedisClient
from backend.src.common.exceptions import ConflictException
from backend.src.core.settings import RedisSettings
from backend.src.core.logger import setup_logger, setup_logger_file_handler, setup_logger_stream_handler
from backend.src.services.gateway import ServiceGateway


logger_file_handler = setup_logger_file_handler(logging.INFO, 'user_service')
logger_stream_handler = setup_logger_stream_handler(logging.INFO)
logger = setup_logger(__name__, logging.INFO, logger_file_handler, logger_stream_handler)


class UpdateUserHandler:
    def __init__(
            self,
            gateway: Annotated[ServiceGateway, Depends(Stub(ServiceGateway))],
            hasher: Annotated[BcryptHasher, Depends(Stub(BcryptHasher))],
            cache: Annotated[RedisClient, Depends(Stub(RedisClient))],
            cache_settings: Annotated[RedisSettings, Depends(Stub(RedisSettings))],
    ) -> None:

        self._gateway = gateway
        self._hasher = hasher
        self._cache = cache
        self._cache_settings = cache_settings

    async def execute(self, current_user: UserInDBSchema, query: UpdateUserQuerySchema) -> UserResponseSchema:
        async with self._gateway:
            try:
                await self._gateway.database.manager.create_transaction()
                return await self._gateway.user().update(
                    query,
                    current_user.id,
                    self._cache_settings.USER_TTL,
                    self._hasher,
                    self._cache
                )

            except IntegrityError as ie:
                logger.error(f'IntegrityError - {ie}')
                raise ConflictException('A user with this data already exists')
