import logging
from typing import cast
from uuid import UUID

from fastapi_example.application.dto import (
    CreateUserDTO,
    DeleteUserDTO,
    UpdateUserDTO,
    UserResponseDTO,
)
from fastapi_example.application.exceptions.http_exceptions import (
    ConflictError,
    ForbiddenError,
    NotFoundError
)
from fastapi_example.application.interfaces.database import ITransactionManager
from fastapi_example.application.interfaces.database.repositories import (
    CreateUserType,
    IUsersRepository,
    UpdateUserType,
)
from fastapi_example.application.interfaces.mappers import IUsersServiceMapper
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

    async def create_user(self, user: CreateUserDTO) -> UserResponseDTO:
        async with self._transaction_manager:
            if await self._repository.exists_user(username=user.username, email=user.email):
                log.warning(
                    "User creation failed - user already exists with username: '%s' or email: '%s'",
                    user.username, user.email
                )
                raise ConflictError(f"User already exists with username: {user.username} or email: {user.email}")

            user.password = self._hasher.hash_password(user.password)
            repository_result = await self._repository.create_user(cast(CreateUserType, user.model_dump()))

        log.info("User created with username: '%s', email: '%s'", user.username, user.email)
        return self._mapper.domain_to_response_dto(repository_result)

    async def get_user(self, user_id: UUID) -> UserResponseDTO:
        async with self._transaction_manager:
            if not await self._repository.exists_user(user_id=user_id):
                log.warning(
                    "User does not exist with ID: '%s'",
                    user_id
                )
                raise NotFoundError("User not found")
            result = await self._repository.get_user(user_id=user_id)

        log.info("User received with ID: %s", result.id)
        return self._mapper.domain_to_response_dto(result)

    async def update_user(self, user_id: UUID, data: UpdateUserDTO) -> UserResponseDTO:
        async with self._transaction_manager:
            if not await self._repository.exists_user(user_id=user_id):
                log.warning(
                    "User does not exist with ID: '%s'",
                    user_id
                )
                raise NotFoundError("User not found")

            current_user = await self._repository.get_user(user_id=user_id)

            if data.username:
                if (data.username != current_user.username) and await self._repository.exists_user(
                        username=data.username):
                    log.warning("User update failed - user already exists with username: '%s'", data.username)
                    raise ConflictError(f"User already exists with username: {data.username}")

            if data.email:
                if (data.email != current_user.email) and await self._repository.exists_user(email=data.email):
                    log.warning("User update failed - user already exists with email: '%s'", data.email)
                    raise ConflictError(f"User already exists with email: {data.email}")

            if data.password:
                data.password = self._hasher.hash_password(data.password)

            user = await self._repository.update_user(
                user_id,
                cast(UpdateUserType, data.model_dump(exclude_unset=True, exclude_none=True))
            )

        log.info("User updated with ID: %s", user.id)
        return self._mapper.domain_to_response_dto(user)

    async def delete_user(self, user_id: UUID, data: DeleteUserDTO) -> UserResponseDTO:
        async with self._transaction_manager:
            if not await self._repository.exists_user(user_id=user_id):
                log.warning(
                    "User does not exist with ID: '%s'",
                    user_id
                )
                raise NotFoundError("User not found")

            current_user = await self._repository.get_user(user_id=user_id)

            if not self._hasher.verify_password(data.password, current_user.password):
                log.warning(
                    "User deletion failed - incorrect password confirmation for user ID: '%s'",
                    user_id
                )
                raise ForbiddenError("Incorrect password confirmation")

            result = await self._repository.delete_user(user_id=user_id)

        log.info("User deleted with ID: %s", result.id)
        return self._mapper.domain_to_response_dto(result)
