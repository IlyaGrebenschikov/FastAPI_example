import logging

from src.application.dto import (
    CreateUserDTO,
    UserResponseDTO,
    UpdateUserDTO
)
from src.application.exceptions.http_exceptions import ConflictError, NotFoundError
from src.application.interfaces.database import ITransactionManager
from src.application.interfaces.database.repositories import IUsersRepository
from src.application.interfaces.mappers import IUsersServiceMapper
from src.application.interfaces.services import (
    IAuthService,
    IUsersService,
    IHasherService,
)

log = logging.getLogger(__name__)


class UsersService(IUsersService):
    def __init__(
            self,
            repository: IUsersRepository,
            mapper: IUsersServiceMapper,
            hasher: IHasherService,
            transaction_manager: ITransactionManager,
            auth: IAuthService,
    ):
        self._repository = repository
        self._mapper = mapper
        self._hasher = hasher
        self._transaction_manager = transaction_manager
        self._auth = auth

    async def create_user(self, user: CreateUserDTO) -> UserResponseDTO:
        log.info(
            "Creating user with username: '%s', email: '%s'",
            user.username, user.email
        )

        async with self._transaction_manager:
            await self._transaction_manager.create_transaction()
            log.debug("Transaction started for user creation")

            if await self._repository.exists_user(username=user.username, email=user.email):
                log.warning(
                    "User creation failed - user already exists with username: '%s' or email: '%s'",
                    user.username, user.email
                )
                raise ConflictError(f"User already exists with username: {user.username} or email: {user.email}")

            user.password = self._hasher.hash_password(user.password)
            log.debug("Hashing password for user '%s'", user.username)

            log.debug(
                "Mapped CreateUserDTO to domain user with ID: %s",
                getattr(user, 'id', 'unknown')
            )

            repository_result = await self._repository.create_user(user.model_dump())

        return self._mapper.domain_to_response_dto(repository_result)

    async def get_user(self, token: str) -> UserResponseDTO:
        user_id = self._auth.get_sub_from_token(token)

        async with self._transaction_manager:
            result = await self._repository.get_user(user_id=user_id)

        if not result:
            log.warning("User retrieval failed - user not found with ID: %s", user_id)
            raise NotFoundError("User not found")

        return self._mapper.domain_to_response_dto(result)

    async def update_user(self, token: str, data: UpdateUserDTO) -> UserResponseDTO:
        user_id = self._auth.get_sub_from_token(token)

        async with self._transaction_manager:
            await self._transaction_manager.create_transaction()
            log.debug("Transaction started for user update")

            current_user = await self._repository.get_user(user_id=user_id)

            if data.username:
                if (data.username != current_user.username) and await self._repository.exists_user(username=data.username):
                    log.warning("User update failed - user already exists with username: '%s'", data.username)
                    raise ConflictError(f"User already exists with username: {data.username}")

            if data.email:
                if (data.email != current_user.email) and await self._repository.exists_user(email=data.email):
                    log.warning("User update failed - user already exists with email: '%s'", data.email)
                    raise ConflictError(f"User already exists with email: {data.email}")

            if data.password:
                data.password = self._hasher.hash_password(data.password)

            user = await self._repository.update_user(user_id, data.model_dump(exclude_unset=True, exclude_none=True))
            log.debug("User updated in repository with ID: %s", user.id)

        return self._mapper.domain_to_response_dto(user)
