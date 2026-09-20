from uuid import UUID

from sqlalchemy import and_, delete, exists, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_example.application.interfaces.database.repositories import (
    IUsersRepository,
    TCreateUser,
    TUpdateUser,
)
from fastapi_example.domain import User
from fastapi_example.infrastructure.database.models import UserModel


def model_to_domain(model: UserModel) -> User:
    return User(id=model.id, email=model.email, password=model.password)


class UsersRepository(IUsersRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_user(self, user: TCreateUser) -> User:
        stmt = insert(UserModel).values(**user).returning(UserModel)
        result = (await self._session.execute(stmt)).scalar_one()
        return model_to_domain(result)

    async def exists_user(
        self,
        user_id: UUID | None = None,
        email: str | None = None,
    ) -> bool:
        if user_id is None and email is None:
            raise ValueError("At least one of user_id or email must be provided")

        conditions = []
        if user_id is not None:
            conditions.append(UserModel.id == user_id)
        if email is not None:
            conditions.append(UserModel.email == email)

        clause = and_(*conditions)
        stmt = exists(select(UserModel).where(clause)).select()
        result = await self._session.scalar(stmt)
        return bool(result)

    async def get_user(
        self,
        user_id: UUID | None = None,
        email: str | None = None,
        for_update: bool = False,
    ) -> User | None:
        if user_id is None and email is None:
            raise ValueError("At least one of user_id or email must be provided")

        conditions = []
        if user_id is not None:
            conditions.append(UserModel.id == user_id)
        if email is not None:
            conditions.append(UserModel.email == email)

        clause = and_(*conditions)
        stmt = select(UserModel).where(clause)
        if for_update:
            stmt = stmt.with_for_update()

        result = (await self._session.execute(stmt)).scalar_one_or_none()
        if not result:
            return None
        return model_to_domain(result)

    async def update_user(
        self,
        user_id: UUID,
        data: TUpdateUser,
    ) -> User | None:
        clause = UserModel.id == user_id
        stmt = update(UserModel).where(clause).values(**data).returning(UserModel)
        result = (await self._session.execute(stmt)).scalar_one_or_none()
        if not result:
            return None
        return model_to_domain(result)

    async def delete_user(
        self,
        user_id: UUID,
    ) -> User | None:
        clause = UserModel.id == user_id
        stmt = delete(UserModel).where(clause).returning(UserModel)
        result = (await self._session.execute(stmt)).scalar_one_or_none()
        if not result:
            return None
        return model_to_domain(result)
