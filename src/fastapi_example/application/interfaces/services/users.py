from typing import Protocol
from uuid import UUID

from fastapi_example.application.dto import (
    DeleteUserDTO,
    UserResponseDTO,
)


class IUsersService(Protocol):
    async def delete_user(
        self, user_id: UUID, data: DeleteUserDTO
    ) -> UserResponseDTO: ...
