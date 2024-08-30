from typing import Type, Any, Optional, Sequence, Mapping, overload

from user_service.src.common.exceptions import InvalidParamsError
from user_service.src.database.repositories.base import BaseRepository
from user_service.src.common.dto.user import UserSchema
from user_service.src.database.models.user import UserModel


class UserRepository(BaseRepository):
    @property
    def model(self) -> Type[UserModel]:
        return UserModel

    async def create(self, **data: UserSchema) -> Optional[UserModel]:
        return await self._crud.insert(**data)

    async def get_one(
            self,
            user_id: Optional[int] = None,
            login: Optional[str] = None,
    ) -> Optional[UserModel]:
        clause = self.model.id == user_id if user_id else self.model.login == login

        return await self._crud.select(clause)

    async def update(self, user_id: Optional[int], **data: UserSchema):
        clause = self.model.id == user_id

        return await self._crud.update(clause, **data)
