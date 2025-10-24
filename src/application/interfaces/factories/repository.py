from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.application.interfaces.repositories import IUsersRepository
from src.application.interfaces.mappers import IUsersRepositoryMapper

class IRepositoriesFactory(Protocol):
    def create_user_repository(self, session_factory: async_sessionmaker[AsyncSession], mapper: IUsersRepositoryMapper) -> IUsersRepository: ...
