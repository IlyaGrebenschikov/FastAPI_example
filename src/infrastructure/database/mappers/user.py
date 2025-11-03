from src.domain.entities.user import User
from src.application.interfaces.mappers import IUsersRepositoryMapper
from src.infrastructure.database.models import UserModel

class UsersRepositoryMapper(IUsersRepositoryMapper):
    def persistence_to_domain(self, model_user: UserModel) -> User:
        return User(
            id=model_user.id,
            username=model_user.username,
            email=model_user.email,
            password=model_user.password,
            created_at=model_user.created_at,
            updated_at=model_user.updated_at,
        )
