from typing import AsyncIterable

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from .base import BaseRepository
from src.domain.entities import User
from src.application.interfaces.mappers import IUsersRepositoryMapper
from src.application.interfaces.repositories import IUsersRepository

class SQLAlchemyUserRepository(BaseRepository, IUsersRepository):
    def __init__(
            self,
            session: AsyncIterable[AsyncSession],
            mapper: IUsersRepositoryMapper
    ):
        super().__init__(session)
        self._mapper = mapper

    async def create_user(self, user: User) -> User:
        sqla_user = self._mapper.domain_to_persistence(user)

        self._session.add(sqla_user)
        await self._session.commit()
        await self._session.refresh(sqla_user)

        return self._mapper.persistence_to_domain(sqla_user)
