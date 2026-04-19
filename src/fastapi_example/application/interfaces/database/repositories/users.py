from typing import Optional, Protocol, TypedDict, NotRequired
from uuid import UUID

from fastapi_example.domain.entities import User

class TCreateUser(TypedDict):
    username: str
    email: str
    password: str


class TUpdateUser(TypedDict):
    username: NotRequired[str]
    email: NotRequired[str]
    password: NotRequired[str]


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
        data: TUpdateUser,
    ) -> User: ...

    async def delete_user(
        self,
        user_id: UUID,
    ) -> User: ...
