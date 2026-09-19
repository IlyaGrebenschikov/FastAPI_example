from .base import BaseDTO


class TokenDTO(BaseDTO):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
