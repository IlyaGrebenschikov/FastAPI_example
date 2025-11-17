from fastapi_example.application.dto import UserResponseDTO
from fastapi_example.application.interfaces.mappers import IUsersServiceMapper
from fastapi_example.domain.entities import User

class UserServiceMapper(IUsersServiceMapper):
    def domain_to_response_dto(self, user: User) -> UserResponseDTO:
        return UserResponseDTO(
            id=user.id,
            username=user.username,
            email=user.email,
            created_at=user.created_at.isoformat(),
            updated_at=user.updated_at.isoformat()
        )
