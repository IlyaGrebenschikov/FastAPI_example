from typing import (
    Optional,
    Type,
)
from uuid import UUID

from sqlalchemy import (
    delete,
    exists,
    insert,
    or_,
    select,
    update,
)
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_example.application.interfaces.database.repositories import (
    IUsersRepository,
    TCreateUser
)
from fastapi_example.application.dto import UpdateUserType
from fastapi_example.application.interfaces.database.repositories.mappers import (
    IUsersRepositoryMapper,
)
from fastapi_example.domain.entities import User
from fastapi_example.infrastructure.database.models import UserModel


class SQLAlchemyUsersRepository(IUsersRepository):
    def __init__(self, session: AsyncSession, mapper: IUsersRepositoryMapper):
        self._session = session
        self._mapper = mapper

    @property
    def _model(self) -> Type[UserModel]:
        return UserModel

    async def create_user(self, user: TCreateUser) -> User:
        stmt = insert(self._model).values(**user).returning(self._model)
        result = (await self._session.execute(stmt)).scalars().first()
        return self._mapper.persistence_to_domain(result)

    async def exists_user(
        self,
        user_id: Optional[UUID] = None,
        username: Optional[str] = None,
        email: Optional[str] = None,
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
        result = await self._session.scalar(stmt)
        return bool(result)

    async def get_user(
        self,
        user_id: Optional[UUID] = None,
        username: Optional[str] = None,
        for_update: bool = False,
    ) -> Optional[User]:
        if not any([user_id, username]):
            raise TypeError("At least one identifier must be provided")

        conditions = []
        if user_id:
            conditions.append(self._model.id == user_id)
        if username:
            conditions.append(self._model.username == username)

        clause = or_(*conditions)
        stmt = select(self._model).where(clause)
        if for_update:
            stmt = stmt.with_for_update()

        result = (await self._session.execute(stmt)).scalar_one_or_none()
        if not result:
            return None
        return self._mapper.persistence_to_domain(result)

    async def update_user(
        self,
        user_id: UUID,
        data: UpdateUserType,
    ) -> User:
        clause = self._model.id == user_id
        stmt = update(self._model).where(clause).values(**data).returning(self._model)
        result = (await self._session.execute(stmt)).scalars().first()
        return self._mapper.persistence_to_domain(result)

    async def delete_user(
        self,
        user_id: UUID,
    ) -> User:
        clause = self._model.id == user_id
        stmt = delete(self._model).where(clause).returning(self._model)
        result = (await self._session.execute(stmt)).scalars().first()
        return self._mapper.persistence_to_domain(result)
