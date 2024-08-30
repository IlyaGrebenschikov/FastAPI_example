from typing import Annotated

from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from user_service.src.utils.providers.stub import Stub
from user_service.src.database.gateway import DBGateway
from user_service.src.common.dto.user import UserSchema, UserResponseSchema, UserInDBSchema
from user_service.src.common.converters.database import from_model_to_dto
from user_service.src.common.exceptions import ConflictException


class DeleteUserHandler:
    def __init__(
            self,
            gateway: Annotated[DBGateway, Depends(Stub(DBGateway))],
    ):
        self._gateway = gateway

    async def execute(self, current_user: UserInDBSchema):
        async with self._gateway:
            await self._gateway.manager.create_transaction()
            result = await self._gateway.user().delete(current_user.id)

            return from_model_to_dto(result, UserResponseSchema)
