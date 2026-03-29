from typing import TypedDict, NotRequired

from .base import BaseSchema


class Token(BaseSchema):
    access_token: str
    token_type: str


class TokenPayload(TypedDict):
    sub: str
    scopes: NotRequired[list[str]]
    exp: NotRequired[int]
    iat: NotRequired[int]


class TokenDecoded(TypedDict):
    sub: str
    exp: int
    iat: int
    scopes: NotRequired[list[str]]