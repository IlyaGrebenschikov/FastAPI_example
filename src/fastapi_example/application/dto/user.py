from typing import Optional
from uuid import UUID

from .base import BaseSchema


class CreateUserDTO(BaseSchema):
    username: str
    email: str
    password: str


class UpdateUserDTO(BaseSchema):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class UserResponseDTO(BaseSchema):
    id: UUID
    username: str
    email: str
    created_at: str
    updated_at: str


class DeleteUserDTO(BaseSchema):
    password: str
