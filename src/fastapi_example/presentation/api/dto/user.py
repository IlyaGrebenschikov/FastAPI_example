from uuid import UUID
from typing import Optional

from pydantic import EmailStr, Field

from .base import BaseDTO


class LoginEmailDTO(BaseDTO):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class CreateUserDTO(BaseDTO):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserResponseDTO(BaseDTO):
    id: UUID
    email: str


class UpdateUserDTO(BaseDTO):
    email: Optional[str] = None
    password: Optional[str] = None


class DeleteUserDTO(BaseDTO):
    password: str
