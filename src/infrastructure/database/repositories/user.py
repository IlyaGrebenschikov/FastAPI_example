from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from .base import BaseRepository
from src.domain.entities import User
from src.application.interfaces.mappers import IUsersRepositoryMapper
from src.application.interfaces.repositories import IUsersRepository

class SQLAlchemyUserRepository(BaseRepository, IUsersRepository):
    def __init__(
            self,
            session_factory: async_sessionmaker[AsyncSession],
            mapper: IUsersRepositoryMapper
    ):
        super().__init__(session_factory)
        self._mapper = mapper

    async def create_user(self, user: User) -> User:
        sqla_user = self._mapper.domain_to_persistence(user)

        async with self._session_factory as session:
            async with session.begin():
                session.add(sqla_user)
                await session.refresh(sqla_user)

        return self._mapper.persistence_to_domain(sqla_user)
