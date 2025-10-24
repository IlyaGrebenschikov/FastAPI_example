from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces.repositories.users_interface import IUserRepository
from src.application.interfaces.mappers import IUsersMapper

class IRepositoryFactory(Protocol):
    def create_user_repository(self, session: AsyncSession, mapper: IUsersMapper) -> IUserRepository: ...
