from typing import Protocol, TypedDict, NotRequired
from uuid import UUID


class TTokenPayload(TypedDict):
    sub: str
    scopes: NotRequired[list[str]]
    exp: NotRequired[int]
    iat: NotRequired[int]


class TTokenDecoded(TypedDict):
    sub: str
    exp: int
    iat: int
    scopes: NotRequired[list[str]]


class ITokenJWTService(Protocol):
    def create_access_token(self, data: TTokenPayload) -> str: ...

    def _verify_token(self, token: str) -> TTokenDecoded: ...

    def get_user_id_from_token(self, token: str) -> UUID: ...
