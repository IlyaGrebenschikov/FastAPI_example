import logging
from datetime import UTC, datetime, timedelta
from typing import cast
from uuid import UUID, uuid4

import jwt

from fastapi_example.application.http_exceptions import UnAuthorizedError
from fastapi_example.application.interfaces.services import (
    AccessTokenClaims,
    ITokenJWTService,
    RefreshTokenClaims,
    TokenClaims,
    TokenData,
    TokenPair,
)
from fastapi_example.core.settings import JWTSettings

log = logging.getLogger(__name__)


class TokenJWTService(ITokenJWTService):
    def __init__(self, settings: JWTSettings) -> None:
        self._settings = settings

    def _encode_token(self, claims: TokenClaims, expire_minutes: int) -> str:
        now = int(datetime.now(UTC).timestamp())
        exp = int((datetime.now(UTC) + timedelta(minutes=expire_minutes)).timestamp())
        return jwt.encode(
            {**claims, "iat": now, "exp": exp},
            self._settings.private_key,
            algorithm=self._settings.algorithm,
        )

    def _create_access_token(self, user_id: UUID) -> str:
        claims: AccessTokenClaims = {"token_type": "access", "sub": str(user_id)}
        return self._encode_token(claims, self._settings.access_expiration)

    def _create_refresh_token(self, user_id: UUID) -> tuple[str, str]:
        jti = str(uuid4())
        claims: RefreshTokenClaims = {
            "token_type": "refresh",
            "sub": str(user_id),
            "jti": jti,
        }
        token = self._encode_token(claims, self._settings.refresh_expiration)
        return token, jti

    def create_token_pair(self, user_id: UUID) -> TokenPair:
        access_token = self._create_access_token(user_id)
        refresh_token, jti = self._create_refresh_token(user_id)
        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token,
            jti=jti,
        )

    def _verify_token(self, token: str) -> TokenClaims:
        try:
            decoded = jwt.decode(
                token, self._settings.public_key, algorithms=[self._settings.algorithm]
            )
        except jwt.ExpiredSignatureError:
            log.warning("Token expired")
            raise UnAuthorizedError("Token expired")
        except jwt.InvalidTokenError as e:
            log.warning("Invalid token: %s", str(e))
            raise UnAuthorizedError("Invalid token")
        return cast(TokenClaims, decoded)

    def verify_access_token(self, token: str) -> UUID:
        claims = self._verify_token(token)
        if claims["token_type"] != "access":
            raise UnAuthorizedError("Access token required")
        return self._parse_user_id(claims["sub"])

    def verify_refresh_token(self, token: str) -> TokenData:
        claims = self._verify_token(token)
        if claims["token_type"] != "refresh":
            raise UnAuthorizedError("Refresh token required")
        claims = cast(RefreshTokenClaims, claims)
        return TokenData(
            user_id=self._parse_user_id(claims["sub"]),
            jti=claims["jti"],
        )

    def _parse_user_id(self, sub: str) -> UUID:
        try:
            return UUID(sub)
        except ValueError:
            log.warning("Invalid token payload")
            raise UnAuthorizedError("Invalid token payload")
