from typing import TypedDict, NotRequired

class TokenPayload(TypedDict):
    sub: str
    scopes: NotRequired[list[str]]


class TokenDecoded(TypedDict):
    sub: str
    exp: int
    iat: int
    scopes: NotRequired[list[str]]
