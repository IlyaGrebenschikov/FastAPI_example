import logging
from dataclasses import dataclass
from uuid import UUID

from fastapi_example.application.http_exceptions import NotFoundError
from fastapi_example.application.interfaces.database import ITransactionManager
from fastapi_example.application.interfaces.database.repositories import (
    IUsersRepository,
)
from fastapi_example.domain import User

log = logging.getLogger(__name__)


@dataclass
class GetUserQuery:
    user_id: UUID


class GetUserHandler:
    def __init__(
        self,
        users_repository: IUsersRepository,
        transaction_manager: ITransactionManager,
    ) -> None:
        self._users_repository = users_repository
        self._transaction_manager = transaction_manager

    async def execute(self, query: GetUserQuery) -> User:
        async with self._transaction_manager:
            user = await self._users_repository.get_user(
                user_id=query.user_id, for_update=False
            )
            if not user:
                log.warning("User does not exist with ID: '%s'", query.user_id)
                raise NotFoundError("User not found")

        log.info("User received with ID: %s", user.id)
        return user
