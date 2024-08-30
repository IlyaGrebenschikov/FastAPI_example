from typing import Type, Any, Optional, Sequence, Mapping

from sqlalchemy import (
    CursorResult,
    select,
    insert,
    update,
    delete
)
from sqlalchemy.ext.asyncio import AsyncSession

from user_service.src.common.interfaces.crud import AbstractCrudRepository
from user_service.src.common.types import ModelType


class CrudRepository(AbstractCrudRepository):
    def __init__(self, session: AsyncSession, model: Type[ModelType]) -> None:
        super().__init__(model)
        self._session = session

    async def select(self, *args: Any) -> Optional[ModelType]:
        stmt = select(self.model).where(*args)
        return (await self._session.execute(stmt)).scalars().first()

    async def select_many(
            self,
            *args: Any,
            offset: Optional[int] = None,
            limit: Optional[int] = None
    ) -> Optional[Sequence[ModelType]]:
        stmt = select(self.model).where(*args).offset(offset).limit(limit)
        return (await self._session.execute(stmt)).scalars().all()

    async def insert(self, **kwargs: Mapping[str, Any]) -> Optional[ModelType]:
        stmt = insert(self.model).values(**kwargs).returning(self.model)
        return (await self._session.execute(stmt)).scalars().first()

    async def insert_many(self, **kwargs: Sequence[Mapping[str, Any]]) -> Optional[Sequence[ModelType]]:
        stmt = insert(self.model).returning(self.model)
        return (await self._session.scalars(stmt, kwargs)).all()

    async def update(self, *args, **kwargs: Mapping[str, Any]) -> Optional[ModelType]:
        stmt = update(self.model).where(*args).values(**kwargs).returning(self.model)
        return (await self._session.execute(stmt)).scalars().first()

    async def update_many(self, data: Sequence[Mapping[str, Any]]) -> CursorResult[Any]:
        return await self._session.execute(update(self.model), data)

    async def delete(self, *args: Any) -> Optional[ModelType]:
        stmt = delete(self.model).where(*args).returning(self.model)
        return (await self._session.execute(stmt)).scalars().all()
