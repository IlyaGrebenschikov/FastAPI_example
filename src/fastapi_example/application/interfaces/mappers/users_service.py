from typing import Protocol

from fastapi_example.application.dto import UserResponseDTO, CreateUserDTO
from fastapi_example.domain.entities import User

class IUsersServiceMapper(Protocol):
    def domain_to_response_dto(self, domain_user: User) -> UserResponseDTO: ...
