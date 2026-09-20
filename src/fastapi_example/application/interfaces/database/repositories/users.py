from typing import Protocol, TypedDict
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
        user_id: UUID | None = None,
        email: str | None = None,
    ) -> bool: ...

    async def get_user(
        self,
        user_id: UUID | None = None,
        email: str | None = None,
        for_update: bool = False,
    ) -> User | None: ...

    async def update_user(
        self,
        user_id: UUID,
        data: TUpdateUser,
    ) -> User | None: ...

    async def delete_user(
        self,
        user_id: UUID,
    ) -> User | None: ...
