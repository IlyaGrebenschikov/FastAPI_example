from typing import NotRequired, Protocol, TypedDict
from uuid import UUID


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


class ITokenJWTService(Protocol):
    def create_access_token(self, data: TokenPayload) -> str: ...

    def _verify_token(self, token: str) -> TokenDecoded: ...

    def get_user_id_from_token(self, token: str) -> UUID: ...
