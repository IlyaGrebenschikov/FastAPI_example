from typing import (
    Type,
    Optional,
    cast
)
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
    exists,
    select,
    or_
)

from .base import BaseRepository
from src.application.interfaces.database.repositories import IUsersRepository
from src.application.interfaces.mappers import IUsersRepositoryMapper
from src.domain.entities import User
from src.infrastructure.database.models import UserModel

class SQLAlchemyUserRepository(BaseRepository, IUsersRepository):
    def __init__(
            self,
            session: AsyncSession,
            mapper: IUsersRepositoryMapper
    ):
        super().__init__(session)
        self._mapper = mapper

    @property
    def _model(self) -> Type[UserModel]:
        return UserModel

    async def create_user(self, user: User) -> User:
        sqla_user = self._mapper.domain_to_persistence(user)

        self._session.add(sqla_user)
        await self._session.flush()
        await self._session.refresh(sqla_user)

        return self._mapper.persistence_to_domain(sqla_user)

    async def exists_user(
            self,
            user_id: Optional[UUID] = None,
            username: Optional[str] = None,
            email: Optional[str] = None
    ) -> bool:
        if not any([user_id, username, email]):
            raise TypeError("At least one identifier must be provided")

        conditions = []
        if user_id:
            conditions.append(self._model.id == user_id)
        if username:
            conditions.append(self._model.username == username)
        if email:
            conditions.append(self._model.email == email)

        clause = or_(*conditions)
        stmt = exists(select(self._model).where(clause)).select()

        return cast(bool, await self._session.scalar(stmt))
