from datetime import datetime
from uuid import uuid4

from src.application.dto import UserResponseDTO, CreateUserDTO
from src.application.interfaces.mappers import IUsersServiceMapper
from src.domain.entities import User

class UserServiceMapper(IUsersServiceMapper):
    def domain_to_response_dto(self, user: User) -> UserResponseDTO:
        return UserResponseDTO(
            id=user.id,
            username=user.username,
            email=user.email,
            created_at=user.created_at.isoformat(),
            updated_at=user.updated_at.isoformat()
        )

    def create_dto_to_domain(self, dto: CreateUserDTO) -> User:
        return User(
            id=uuid4(),
            username=dto.username,
            email=dto.email,
            password=dto.password,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
