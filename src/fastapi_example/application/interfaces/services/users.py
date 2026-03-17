from typing import Protocol

from fastapi_example.application.dto import (
    CreateUserDTO,
    DeleteUserDTO,
    UpdateUserDTO,
    UserResponseDTO,
)


class IUsersService(Protocol):
    async def create_user(self, user: CreateUserDTO) -> UserResponseDTO: ...

    async def get_user(self, token: str) -> UserResponseDTO: ...

    async def update_user(
            self,
            token: str,
            data: UpdateUserDTO,
    ) -> UserResponseDTO: ...

    async def delete_user(self, token: str, data: DeleteUserDTO) -> UserResponseDTO: ...
