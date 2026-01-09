from typing import (
    Optional,
    Unpack,
    Type,
)
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
    delete,
    exists,
    select,
    insert,
    or_,
    update,
)

from .base import BaseRepository
from fastapi_example.application.interfaces.database.repositories import IUsersRepository
from fastapi_example.application.interfaces.mappers import IUsersRepositoryMapper
from fastapi_example.application.types import CreateUserType, UpdateUserType
from fastapi_example.domain.entities import User
from fastapi_example.infrastructure.database.models import UserModel

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

    async def create_user(self, user: Unpack[CreateUserType]) -> User:
        stmt = insert(self._model).values(user).returning(self._model)

        return self._mapper.persistence_to_domain((await self._session.scalars(stmt)).first())

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

        return await self._session.scalar(stmt)

    async def get_user(
            self,
            user_id: Optional[UUID | str] = None,
            username: Optional[str] = None,
    ) -> User:
        if not any([user_id, username]):
            raise TypeError("At least one identifier must be provided")

        conditions = []
        if user_id:
            conditions.append(self._model.id == user_id)
        if username:
            conditions.append(self._model.username == username)

        clause = or_(*conditions)
        stmt = select(self._model).where(clause)

        return self._mapper.persistence_to_domain((await self._session.execute(stmt)).scalars().first())

    async def update_user(
            self,
            user_id: UUID | str,
            data: Unpack[UpdateUserType],
    ) -> User:
        clause = self._model.id == user_id
        stmt = update(self._model).where(clause).values(**data).returning(self._model)

        return self._mapper.persistence_to_domain((await self._session.execute(stmt)).scalars().first())

    async def delete_user(
            self,
            user_id: UUID | str,
    ) -> User:
        clause = self._model.id == user_id
        stmt = delete(self._model).where(clause).returning(self._model)

        return self._mapper.persistence_to_domain((await self._session.execute(stmt)).scalars().first())
