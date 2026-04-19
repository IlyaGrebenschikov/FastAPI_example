from uuid import UUID
from datetime import datetime
from typing import Optional

from .base import BaseSchema


class CreateUserDTO(BaseSchema):
    username: str
    email: str
    password: str


class UserResponseDTO(BaseSchema):
    id: UUID
    username: str
    email: str
    created_at: datetime
    updated_at: datetime


class UpdateUserDTO(BaseSchema):
    username: Optional[str] = None
    email: Optional[str] = None
