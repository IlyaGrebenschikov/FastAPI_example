from typing import Protocol

from src.domain.entities import User

class IUserRepository(Protocol):
    async def create_user(self, user: User) -> User: ...
