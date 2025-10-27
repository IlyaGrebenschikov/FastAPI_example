from __future__ import annotations

from types import TracebackType
from typing import Optional, Type, Union

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncSessionTransaction,
    async_sessionmaker,
)

from .exceptions import CommitError, RollbackError
from src.application.interfaces.database import ITransactionManager

class TransactionManager(ITransactionManager):
    __slots__ = (
        "_session",
        "_transaction",
    )

    def __init__(
        self, session_or_factory: Union[AsyncSession, async_sessionmaker[AsyncSession]]
    ) -> None:
        if isinstance(session_or_factory, async_sessionmaker):
            self._session = session_or_factory()
        else:
            self._session = session_or_factory

        self._transaction: Optional[AsyncSessionTransaction] = None

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        if self._transaction:
            if exc_type:
                await self.rollback()
            else:
                await self.commit()

        await self.close_transaction()

    async def __aenter__(self) -> TransactionManager:
        return self

    async def commit(self) -> None:
        try:
            await self._session.commit()
        except SQLAlchemyError as err:
            raise CommitError from err

    async def rollback(self) -> None:
        try:
            await self._session.rollback()
        except SQLAlchemyError as err:
            raise RollbackError from err

    async def create_transaction(self) -> None:
        if not self._session.in_transaction() and self._session.is_active:
            self._transaction = await self._session.begin()

    async def close_transaction(self) -> None:
        if self._session.is_active:
            await self._session.close()

    @property
    def session(self) -> AsyncSession:
        return self._session
