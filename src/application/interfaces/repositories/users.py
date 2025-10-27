from typing import (
    Protocol,
    Optional,
)
from uuid import UUID

from src.domain.entities import User

class IUsersRepository(Protocol):
    async def create_user(self, user: User) -> User: ...

    async def exists_user(
            self,
            user_id: Optional[UUID] = None,
            username: Optional[str] = None,
            email: Optional[str] = None
    ) -> bool: ...
