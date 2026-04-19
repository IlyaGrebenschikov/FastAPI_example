import logging
from uuid import UUID

from fastapi_example.application.dto import (
    DeleteUserDTO,
    UserResponseDTO,
)
from fastapi_example.application.exceptions.http_exceptions import (
    ForbiddenError,
    NotFoundError,
)
from fastapi_example.application.interfaces.database import ITransactionManager
from fastapi_example.application.interfaces.database.repositories import (
    IUsersRepository,
)
from fastapi_example.application.interfaces.services.mappers import IUsersServiceMapper
from fastapi_example.application.interfaces.security import IHasher
from fastapi_example.application.interfaces.services import IUsersService

log = logging.getLogger(__name__)


class UsersService(IUsersService):
    def __init__(
        self,
        repository: IUsersRepository,
        mapper: IUsersServiceMapper,
        hasher: IHasher,
        transaction_manager: ITransactionManager,
    ):
        self._repository = repository
        self._mapper = mapper
        self._hasher = hasher
        self._transaction_manager = transaction_manager


    async def delete_user(
        self, user_id: UUID, data: DeleteUserDTO, for_update: bool = True
    ) -> UserResponseDTO:
        async with self._transaction_manager:
            user = await self._repository.get_user(
                user_id=user_id, for_update=for_update
            )
            if not user:
                log.warning("User does not exist with ID: '%s'", user_id)
                raise NotFoundError("User not found")

            if not self._hasher.verify_password(data.password, user.password):
                log.warning(
                    "User deletion failed - incorrect password confirmation for user ID: '%s'",
                    user_id,
                )
                raise ForbiddenError("Incorrect password confirmation")

            result = await self._repository.delete_user(user_id=user_id)

        log.info("User deleted with ID: %s", result.id)
        return self._mapper.domain_to_response_dto(result)
