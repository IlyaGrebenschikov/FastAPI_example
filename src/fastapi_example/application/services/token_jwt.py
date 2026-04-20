import logging
from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import UUID

import jwt

from fastapi_example.application.exceptions.http_exceptions import UnAuthorizedError
from fastapi_example.application.interfaces.services import (
    ITokenJWTService,
    TTokenDecoded,
    TTokenPayload
)
from fastapi_example.infrastructure.settings import JWTSettings

log = logging.getLogger(__name__)


class TokenJWTService(ITokenJWTService):
    def __init__(self, settings: JWTSettings) -> None:
        self._settings = settings

    def create_access_token(self, data: TTokenPayload) -> str:
        to_encode: dict[str, Any] = {}
        to_encode.update(data)
        expiration = datetime.now(timezone.utc) + timedelta(
            minutes=self._settings.expiration
        )
        to_encode.update(
            {
                "exp": int(expiration.timestamp()),
                "iat": int(datetime.now(timezone.utc).timestamp()),
            }
        )
        token = jwt.encode(
            to_encode, self._settings.private_key, algorithm=self._settings.algorithm
        )

        log.info(
            "Access token created for subject '%s', expires at %s",
            data.get("sub", "unknown"),
            expiration.isoformat(),
        )
        return token

    def _verify_token(self, token: str) -> TTokenDecoded:
        try:
            decoded_data: TTokenDecoded = jwt.decode(
                token, self._settings.public_key, algorithms=[self._settings.algorithm]
            )
        except jwt.ExpiredSignatureError:
            log.warning("Token expired")
            raise UnAuthorizedError("Token expired")

        except jwt.InvalidTokenError as e:
            log.warning("Invalid token: %s", str(e))
            raise UnAuthorizedError("Invalid token")

        if not decoded_data.get("sub"):
            log.warning("Token missing subject field")
            raise UnAuthorizedError("Token missing subject")

        log.debug(
            "Token successfully decoded for subject '%s'",
            decoded_data.get("sub", "unknown"),
        )
        return decoded_data

    def get_user_id_from_token(self, token: str) -> UUID:
        token_data = self._verify_token(token)
        user_id = UUID(token_data.get("sub"))

        if not user_id:
            log.warning("Token missing subject field")
            raise UnAuthorizedError("Token missing subject")

        return user_id
