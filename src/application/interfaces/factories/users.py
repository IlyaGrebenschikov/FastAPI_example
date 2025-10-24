from typing import Protocol

from src.domain.entities.user import User
from src.application.dto import CreateUserDTO

class IUsersFactory(Protocol):
    def create_user(self, dto: CreateUserDTO) -> User: ...