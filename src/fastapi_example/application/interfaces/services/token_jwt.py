from dataclasses import dataclass
from typing import Literal, NotRequired, Protocol, TypedDict
from uuid import UUID


class AccessTokenClaims(TypedDict):
    token_type: Literal["access"]
    sub: str
    jti: NotRequired[str]
    iat: NotRequired[int]
    exp: NotRequired[int]


class RefreshTokenClaims(TypedDict):
    token_type: Literal["refresh"]
    sub: str
    jti: str
    iat: NotRequired[int]
    exp: NotRequired[int]


TokenClaims = AccessTokenClaims | RefreshTokenClaims


@dataclass(frozen=True)
class TokenData:
    user_id: UUID
    jti: str


@dataclass(frozen=True)
class TokenPair:
    access_token: str
    refresh_token: str
    jti: str


class ITokenJWTService(Protocol):
    def create_token_pair(self, user_id: UUID) -> TokenPair: ...

    def verify_access_token(self, token: str) -> UUID: ...

    def verify_refresh_token(self, token: str) -> TokenData: ...
