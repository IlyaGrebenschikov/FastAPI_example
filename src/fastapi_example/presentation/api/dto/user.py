from uuid import UUID

from pydantic import EmailStr, Field

from .base import BaseDTO, BaseResponseDTO


class CreateUserDTO(BaseDTO):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UpdateUserDTO(BaseDTO):
    email: str | None = None
    password: str | None = None


class DeleteUserDTO(BaseDTO):
    password: str


class UserResponseDTO(BaseResponseDTO):
    id: UUID
    email: str
