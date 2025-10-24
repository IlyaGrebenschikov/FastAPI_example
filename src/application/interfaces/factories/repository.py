from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces.repositories import IUsersRepository
from src.application.interfaces.mappers import IUsersRepositoryMapper

class IRepositoriesFactory(Protocol):
    def create_user_repository(self, session: AsyncSession, mapper: IUsersRepositoryMapper) -> IUsersRepository: ...
