from datetime import datetime
from typing import Optional
from typing_extensions import Self

from pydantic import EmailStr, BaseModel, field_validator, model_validator


class UserSchema(BaseModel):
    login: str
    email: EmailStr
    password: str

    @field_validator("password")
    def check_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must have at least 8 characters")

        if not any(c.isupper() for c in value):
            raise ValueError("Password must have at least one uppercase letter")

        if not any(c.islower() for c in value):
            raise ValueError("Password must have at least one lowercase letter")

        if not any(c.isdigit() for c in value):
            raise ValueError("Password must have at least one digit")

        return value


class UserInDBSchema(UserSchema):
    id: int
    is_superuser: bool
    created_at: datetime
    updated_at: datetime


class UserResponseSchema(BaseModel):
    login: str
    email: EmailStr


class GetUserQuerySchema(BaseModel):
    id: Optional[int] = None
    login: Optional[str] = None


class UpdateUserQuerySchema(UserSchema):
    login: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    @model_validator(mode='after')
    def check_at_least_one_field(self) -> Self:
        if not any(value is not None for value in (self.login, self.email, self.password)):
            raise ValueError('At least one field must be provided')

        return self
