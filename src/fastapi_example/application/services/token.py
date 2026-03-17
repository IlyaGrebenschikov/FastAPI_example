import logging
from uuid import UUID

from fastapi_example.application.exceptions.http_exceptions import UnAuthorizedError
from fastapi_example.application.interfaces.database import ITransactionManager
from fastapi_example.application.interfaces.database.repositories import (
    IUsersRepository,
)
from fastapi_example.application.interfaces.services import (
    ITokenJWTService,
    ITokenService,
)

log = logging.getLogger(__name__)


class TokenService(ITokenService):
    def __init__(
            self,
            user_repository: IUsersRepository,
            token_jwt: ITokenJWTService,
            transaction_manager: ITransactionManager
    ) -> None:
        self._user_repository = user_repository
        self._token_jwt = token_jwt
        self._transaction_manager = transaction_manager

    async def get_user_id_from_token(self, token: str) -> UUID:
        token_data = self._token_jwt.verify_token(token)
        sub = token_data.get("sub")

        if not sub:
            log.warning("Token missing subject field")
            raise UnAuthorizedError('Token missing subject')

        try:
            user_id = UUID(sub)
        except ValueError:
            log.warning("Invalid UUID in token subject: '%s'", sub)
            raise UnAuthorizedError('Invalid token subject')

        async with self._transaction_manager.read_only():
            if not await self._user_repository.exists_user(user_id=user_id):
                log.warning(
                    "Token validation failed - user does not exist with ID: '%s'",
                    user_id
                )
                raise UnAuthorizedError("User not found")

        log.debug("Extracted and verified subject '%s' from token", user_id)
        return user_id
