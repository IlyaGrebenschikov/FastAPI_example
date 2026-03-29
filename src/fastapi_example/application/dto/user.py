from typing import Optional, TypedDict, NotRequired
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


class UpdateUserType(TypedDict):
    username: NotRequired[str]
    email: NotRequired[str]
    password: NotRequired[str]


class CreateUserType(TypedDict):
    username: str
    email: str
    password: str
