import logging

from fastapi_example.application.exceptions.http_exceptions import UnAuthorizedError
from fastapi_example.application.interfaces.database import ITransactionManager
from fastapi_example.application.interfaces.database.repositories import IUsersRepository
from fastapi_example.application.interfaces.services import (
    ITokenJWTService,
    ITokenService
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

    async def get_user_id_from_token(self, token: str) -> str:
        token_data = self._token_jwt.verify_token(token)
        sub = token_data.get("sub")

        if not sub:
            log.warning("Token missing subject field")
            raise UnAuthorizedError('Token missing subject')

        async with self._transaction_manager.read_only():
            if not await self._user_repository.exists_user(user_id=sub):
                log.warning(
                    "Token validation failed - user does not exist with ID: '%s'",
                    sub
                )
                raise UnAuthorizedError("User not found")

        log.debug("Extracted and verified subject '%s' from token", sub)
        return sub
