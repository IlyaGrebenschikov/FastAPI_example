from pydantic import EmailStr, Field

from .base import BaseDTO, BaseResponseDTO


class LoginEmailDTO(BaseDTO):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class TokenResponseDTO(BaseResponseDTO):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class LogoutResponseDTO(BaseResponseDTO):
    message: str = "logged out"
