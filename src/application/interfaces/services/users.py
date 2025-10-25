from typing import Protocol

from src.application.dto import CreateUserDTO, UserResponseDTO

class IUsersService(Protocol):
    async def create_user(self, user: CreateUserDTO) -> UserResponseDTO: ...
