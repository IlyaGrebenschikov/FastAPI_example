from src.application.dto import (
    CreateUserDTO,
    UserResponseDTO
)
from src.application.interfaces.mappers import IUsersServiceMapper
from src.application.interfaces.repositories import IUsersRepository
from src.application.interfaces.services import IUsersService

class UsersService(IUsersService):
    def __init__(
            self,
            repository: IUsersRepository,
            mapper: IUsersServiceMapper
    ):
        self._repository = repository
        self._mapper = mapper

    async def create_user(self, user: CreateUserDTO) -> UserResponseDTO:
        domain_user = self._mapper.create_dto_to_domain(user)
        repository_result = await self._repository.create_user(domain_user)
        return self._mapper.domain_to_response_dto(repository_result)
