from typing import Type, Any, Optional, Sequence, Mapping

from user_service.src.database.repositories.base import BaseRepository
from user_service.src.common.dto.user import UserSchema
from user_service.src.database.models.user import UserModel


class UserRepository(BaseRepository):
    @property
    def model(self) -> Type[UserModel]:
        return UserModel

    async def create(self, **data: UserSchema) -> Optional[UserModel]:
        return await self._crud.insert(**data)
