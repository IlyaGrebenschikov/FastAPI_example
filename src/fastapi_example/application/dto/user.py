from typing import Optional, TypedDict, NotRequired
from uuid import UUID

from .base import BaseSchema


class UserResponseDTO(BaseSchema):
    id: UUID
    username: str
    email: str
    created_at: str
    updated_at: str


class DeleteUserDTO(BaseSchema):
    password: str
