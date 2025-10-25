from typing import Protocol

from src.application.dto import UserResponseDTO, CreateUserDTO
from src.domain.entities import User

class IUsersServiceMapper(Protocol):
    def domain_to_response_dto(self, domain_user: User) -> UserResponseDTO: ...

    def create_dto_to_domain(self, create_dto_user: CreateUserDTO) -> User: ...
