from .base import BaseDTO, BaseResponseDTO


class LoginEmailDTO(BaseDTO):
    email: str
    password: str


class TokenResponseDTO(BaseResponseDTO):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class LogoutResponseDTO(BaseResponseDTO):
    message: str = "logged out"
