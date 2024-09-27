import logging

from typing import Annotated

from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from backend.src.utils.providers.stub import Stub
from backend.src.database.gateway import DBGateway
from backend.src.common.dto.user import UserSchema, UserResponseSchema
from backend.src.services.security.bcrypt_hasher import BcryptHasher
from backend.src.common.converters.database import from_model_to_dto
from backend.src.common.exceptions import ConflictException
from backend.src.core.logger import setup_logger, setup_logger_file_handler, setup_logger_stream_handler
from backend.src.core.settings import get_logger_settings


logger_settings = get_logger_settings()
logger_file_handler = setup_logger_file_handler(logger_settings, logging.INFO, 'user_service')
logger_stream_handler = setup_logger_stream_handler(logger_settings, logging.INFO)
logger = setup_logger(__name__, logging.INFO, logger_file_handler, logger_stream_handler)


class CreateUserHandler:
    def __init__(
            self,
            gateway: Annotated[DBGateway, Depends(Stub(DBGateway))],
            hasher: Annotated[BcryptHasher, Depends(Stub(BcryptHasher))],
    ) -> None:
        self._gateway = gateway
        self._hasher = hasher

    async def execute(self, query: UserSchema) -> UserResponseSchema:
        query.password = self._hasher.hash_password(query.password)

        async with self._gateway:
            try:
                await self._gateway.manager.create_transaction()
                result = await self._gateway.user().create(**query.model_dump())

                return from_model_to_dto(result, UserResponseSchema)

            except IntegrityError as ie:
                logger.error(f'IntegrityError - {ie}')
                raise ConflictException('This user already exists')
