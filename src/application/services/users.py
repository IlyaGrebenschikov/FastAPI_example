import logging

from src.application.dto import (
    CreateUserDTO,
    UserResponseDTO
)
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

    # TODO need custom http exceptions
    async def create_user(self, user: CreateUserDTO) -> UserResponseDTO:
        async with self._transaction_manager:
            await self._transaction_manager.create_transaction()
            if await self._repository.exists_user(username=user.username, email=user.email):
                log.info("Attempt to create user with existing credentials")
                raise ValueError(f'User {user.username} already exists')

            user.password = self._hasher.hash_password(user.password)

            domain_user = self._mapper.create_dto_to_domain(user)
            repository_result = await self._repository.create_user(domain_user)

        return self._mapper.domain_to_response_dto(repository_result)
