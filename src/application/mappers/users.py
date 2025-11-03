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
