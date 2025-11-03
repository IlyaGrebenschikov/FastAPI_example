from typing import Protocol

from src.application.dto import CreateUserDTO, UserResponseDTO, UpdateUserDTO

class IUsersService(Protocol):
    async def create_user(self, user: CreateUserDTO) -> UserResponseDTO: ...

    async def get_user(self, token: str) -> UserResponseDTO: ...

    async def update_user(
            self,
            token: str,
            data: UpdateUserDTO,
    ) -> UserResponseDTO: ...
