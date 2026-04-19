from typing import Optional, Protocol, TypedDict
from uuid import UUID

from fastapi_example.domain.entities import User
from fastapi_example.application.dto import UpdateUserType

class TCreateUser(TypedDict):
    username: str
    email: str
    password: str


class IUsersRepository(Protocol):
    async def create_user(self, user: TCreateUser) -> User: ...

    async def exists_user(
        self,
        user_id: Optional[UUID] = None,
        username: Optional[str] = None,
        email: Optional[str] = None,
    ) -> bool: ...

    async def get_user(
        self,
        user_id: Optional[UUID] = None,
        username: Optional[str] = None,
        for_update: bool = False,
    ) -> Optional[User]: ...

    async def update_user(
        self,
        user_id: UUID,
        data: UpdateUserType,
    ) -> User: ...

    async def delete_user(
        self,
        user_id: UUID,
    ) -> User: ...
