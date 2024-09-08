from typing import Annotated

from fastapi import Depends

from backend.src.utils.providers.stub import Stub
from backend.src.database.gateway import DBGateway
from backend.src.common.dto.user import UserResponseSchema, UserInDBSchema
from backend.src.common.converters.database import from_model_to_dto


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
