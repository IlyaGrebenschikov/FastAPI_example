from .base import BaseSchema


class TokenDTO(BaseSchema):
    access_token: str
    token_type: str
