from typing import Protocol, TypedDict, NotRequired

class TokenPayload(TypedDict):
    sub: str
    scopes: NotRequired[list[str]]


class TokenDecoded(TypedDict):
    sub: str
    exp: int
    iat: int
    scopes: NotRequired[list[str]]


class ITokenJWTService(Protocol):
    def create_access_token(self, data: TokenPayload) -> str: ...

    def verify_token(self, token: str) -> TokenDecoded: ...
