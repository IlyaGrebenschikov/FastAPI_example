from typing import (
    Protocol,
    Optional,
    Unpack
)
from uuid import UUID

from fastapi_example.application.types import UpdateUserType, CreateUserType
from fastapi_example.domain.entities import User

class IUsersRepository(Protocol):
    async def create_user(self, user: Unpack[CreateUserType]) -> User: ...

    async def exists_user(
            self,
            user_id: Optional[UUID | str] = None,
            username: Optional[str] = None,
            email: Optional[str] = None
    ) -> bool: ...

    async def get_user(
            self,
            user_id: Optional[UUID | str] = None,
            username: Optional[str] = None,
    ) -> User: ...

    async def update_user(
            self,
            user_id: UUID | str,
            data: Unpack[UpdateUserType],
    ) -> User: ...

    async def delete_user(
            self,
            user_id: UUID | str,
    ) -> User: ...
