import logging
from datetime import (
    datetime,
    timedelta,
    timezone
)

import jwt

from src.application.exceptions.http_exceptions import UnAuthorizedError
from src.application.interfaces.services import ITokenJWTService
from src.application.settings import JWTSettings

log = logging.getLogger(__name__)


# TODO need typed dict for return annotation
class TokenJWTService(ITokenJWTService):
    def __init__(self, settings: JWTSettings) -> None:
        self._settings = settings

    def create_access_token(self, data: dict) -> str:
        log.debug(
            "Creating access token for subject '%s'",
            data.get('sub', 'unknown')
        )

        to_encode = data.copy()
        expiration = datetime.now(timezone.utc) + timedelta(minutes=self._settings.expiration)
        to_encode.update({
            "exp": expiration,
            "iat": datetime.now(timezone.utc)
        })
        token = jwt.encode(
            to_encode,
            self._settings.private_key,
            algorithm=self._settings.algorithm
        )

        log.info(
            "Access token created for subject '%s', expires at %s",
            data.get('sub', 'unknown'),
            expiration.isoformat()
        )

        return token


    def verify_token(self, token: str) -> dict:
        log.debug("Verifying token")

        try:
            decoded_data = jwt.decode(
                token,
                self._settings.public_key,
                algorithms=[self._settings.algorithm]
            )

            log.debug(
                "Token successfully decoded for subject '%s'",
                decoded_data.get('sub', 'unknown')
            )

        except jwt.ExpiredSignatureError:
            log.warning("Token expired")
            raise UnAuthorizedError('Token expired')

        except jwt.InvalidTokenError as e:
            log.warning("Invalid token: %s", str(e))
            raise UnAuthorizedError('Invalid token')

        if not decoded_data.get('sub'):
            log.warning("Token missing subject field")
            raise UnAuthorizedError('Token missing subject')

        return decoded_data
