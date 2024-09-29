import logging

from typing import Annotated

from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from backend.src.utils.providers.stub import Stub
from backend.src.common.dto.user import UserSchema, UserResponseSchema
from backend.src.services.security.bcrypt_hasher import BcryptHasher
from backend.src.common.exceptions import ConflictException
from backend.src.core.logger import setup_logger, setup_logger_file_handler, setup_logger_stream_handler
from backend.src.services.gateway import ServiceGateway

logger_file_handler = setup_logger_file_handler(logging.INFO, 'user_service')
logger_stream_handler = setup_logger_stream_handler(logging.INFO)
logger = setup_logger(__name__, logging.INFO, logger_file_handler, logger_stream_handler)


class CreateUserHandler:
    def __init__(
            self,
            hasher: Annotated[BcryptHasher, Depends(Stub(BcryptHasher))],
            gateway: Annotated[ServiceGateway, Depends(Stub(ServiceGateway))]
    ) -> None:
        self._gateway = gateway
        self._hasher = hasher

    async def execute(self, query: UserSchema) -> UserResponseSchema:
        async with self._gateway:
            try:
                await self._gateway.database.manager.create_transaction()
                return await self._gateway.user().create(query, self._hasher)

            except IntegrityError as ie:
                logger.error(f'IntegrityError - {ie}')
                raise ConflictException('This user already exists')
