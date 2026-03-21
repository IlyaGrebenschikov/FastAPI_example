from typing import Protocol
from uuid import UUID

from fastapi_example.application.dto import (
    CreateUserDTO,
    DeleteUserDTO,
    UpdateUserDTO,
    UserResponseDTO,
)


class IUsersService(Protocol):
    async def create_user(self, user: CreateUserDTO) -> UserResponseDTO: ...

    async def get_user(self, user_id: UUID) -> UserResponseDTO: ...

    async def update_user(self, user_id: UUID, data: UpdateUserDTO) -> UserResponseDTO: ...

    async def delete_user(self, user_id: UUID, data: DeleteUserDTO) -> UserResponseDTO: ...
