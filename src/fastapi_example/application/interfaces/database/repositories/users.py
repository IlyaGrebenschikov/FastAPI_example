from typing import (
    Protocol,
    Optional,
    TypedDict,
    NotRequired
)
from uuid import UUID

from fastapi_example.domain.entities import User

class UpdateUserType(TypedDict):
    username: NotRequired[str]
    email: NotRequired[str]
    password: NotRequired[str]


class CreateUserType(TypedDict):
    username: str
    email: str
    password: str


class IUsersRepository(Protocol):
    async def create_user(self, user: CreateUserType) -> User: ...

    async def exists_user(
            self,
            user_id: Optional[UUID] = None,
            username: Optional[str] = None,
            email: Optional[str] = None
    ) -> bool: ...

    async def get_user(
            self,
            user_id: Optional[UUID] = None,
            username: Optional[str] = None,
    ) -> User: ...

    async def update_user(
            self,
            user_id: UUID,
            data: UpdateUserType,
    ) -> User: ...

    async def delete_user(
            self,
            user_id: UUID,
    ) -> User: ...

