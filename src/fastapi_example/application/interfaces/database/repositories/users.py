from typing import Optional, Protocol, TypedDict
from uuid import UUID

from fastapi_example.domain import User


class TCreateUser(TypedDict):
    email: str
    password: str


class TUpdateUser(TypedDict, total=False):
    email: str
    password: str


class IUsersRepository(Protocol):
    async def create_user(self, user: TCreateUser) -> User: ...

    async def exists_user(
        self,
        user_id: Optional[UUID] = None,
        email: Optional[str] = None,
    ) -> bool: ...

    async def get_user(
        self,
        user_id: Optional[UUID] = None,
        email: Optional[str] = None,
        for_update: bool = False,
    ) -> Optional[User]: ...

    async def update_user(
        self,
        user_id: UUID,
        data: TUpdateUser,
    ) -> Optional[User]: ...

    async def delete_user(
        self,
        user_id: UUID,
    ) -> Optional[User]: ...
