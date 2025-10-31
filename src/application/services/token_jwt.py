from datetime import (
    datetime,
    timedelta,
    timezone
)

import jwt

from src.application.exceptions.http_exceptions import UnAuthorizedError
from src.application.interfaces.services import ITokenJWTService
from src.application.settings import JWTSettings

# TODO need typed dict for return annotation
class TokenJWTService(ITokenJWTService):
    def __init__(self, settings: JWTSettings) -> None:
        self._settings = settings

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        to_encode.update({
            "exp": datetime.now(timezone.utc) + timedelta(minutes=self._settings.expiration),
            "iat": datetime.now(timezone.utc)
        })
        return jwt.encode(
            to_encode,
            self._settings.private_key,
            algorithm=self._settings.algorithm
        )

    def verify_token(self, token: str) -> dict:
        try:
            decoded_data = jwt.decode(
                token,
                self._settings.public_key,
                algorithms=[self._settings.algorithm]
            )

        except jwt.ExpiredSignatureError:
            raise UnAuthorizedError('Token expired')

        except jwt.InvalidTokenError:
            raise UnAuthorizedError('Invalid token')

        if not decoded_data.get('sub'):
            raise UnAuthorizedError('Token missing subject')

        return decoded_data
