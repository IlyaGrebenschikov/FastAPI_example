import logging

from src.application.dto import (
    CreateUserDTO,
    UserResponseDTO
)
from src.application.exceptions.http_exceptions import ConflictError
from src.application.interfaces.database import ITransactionManager
from src.application.interfaces.database.repositories import IUsersRepository
from src.application.interfaces.mappers import IUsersServiceMapper
from src.application.interfaces.services import (
    IUsersService,
    IHasherService
)

log = logging.getLogger(__name__)


class UsersService(IUsersService):
    def __init__(
            self,
            repository: IUsersRepository,
            mapper: IUsersServiceMapper,
            hasher: IHasherService,
            transaction_manager: ITransactionManager
    ):
        self._repository = repository
        self._mapper = mapper
        self._hasher = hasher
        self._transaction_manager = transaction_manager

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

            domain_user = self._mapper.create_dto_to_domain(user)
            log.debug(
                "Mapped CreateUserDTO to domain user with ID: %s",
                getattr(domain_user, 'id', 'unknown')
            )

            repository_result = await self._repository.create_user(domain_user)
            log.debug("User created in repository with ID: %s", repository_result.id)

        return self._mapper.domain_to_response_dto(repository_result)
