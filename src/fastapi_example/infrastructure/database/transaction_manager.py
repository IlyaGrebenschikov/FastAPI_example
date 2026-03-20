from __future__ import annotations

from types import TracebackType
from typing import (
    Optional,
    Type,
)

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncSessionTransaction,
)

from fastapi_example.application.interfaces.database import ITransactionManager
from .exceptions import CommitError, RollbackError


class TransactionManager(ITransactionManager[AsyncSession]):
    __slots__ = ("_session", "_transaction")

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._transaction: Optional[AsyncSessionTransaction] = None

    async def __aenter__(self) -> TransactionManager:
        if self._session.in_transaction():
            raise RuntimeError("Session already in transaction")
        self._transaction = await self._session.begin()
        return self

    async def __aexit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_value: Optional[BaseException],
            traceback: Optional[TracebackType],
    ) -> None:
        if not self._transaction:
            return

        try:
            if exc_type:
                await self._session.rollback()
            else:
                await self._session.commit()
        except SQLAlchemyError as err:
            raise (RollbackError if exc_type else CommitError)(err) from err
        finally:
            self._transaction = None
