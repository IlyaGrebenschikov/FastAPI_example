import logging

from fastapi_example.application.interfaces.database import ITransactionManager
from fastapi_example.application.interfaces.database.repositories import IUsersRepository
from .query import GetUserQuery
from fastapi_example.domain.entities import User
from fastapi_example.application.exceptions.http_exceptions import NotFoundError

log = logging.getLogger(__name__)


class GetUserHandler:
    def __init__(self, repository: IUsersRepository, transaction_manager: ITransactionManager) -> None:
        self._repository = repository
        self._transaction_manager = transaction_manager

    async def execute(
        self, query: GetUserQuery
    ) -> User:
        async with self._transaction_manager:
            user = await self._repository.get_user(
                user_id=query.user_id, for_update=False
            )
            if not user:
                log.warning("User does not exist with ID: '%s'", query.user_id)
                raise NotFoundError("User not found")

        log.info("User received with ID: %s", user.id)
        return user
