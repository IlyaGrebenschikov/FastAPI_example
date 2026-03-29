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
    """
    Async context manager for explicit transaction control.

    Guarantees atomic database operations by wrapping code in a transaction.
    Commits on successful exit, rolls back on exception.

    Usage in services:
       async def create_user(self, dto: CreateUserDTO) -> User:
           async with self._transaction_manager:
               # All database operations here are atomic
               user = await self._repository.create(dto)
               await self._audit.log("user_created", user.id)
               return user
           # Automatically committed here, or rolled back if exception occurred

    Important:
       - Session must NOT be in transaction before entering context (no autobegin)
       - All database operations should be inside the async with block
       - Session lifecycle is managed by DI, not this manager
       - Supports sequential transactions (multiple async with blocks per request)
       - Nested transactions are NOT supported (will raise RuntimeError)

    Raises:
       RuntimeError: If session already has active transaction (autobegin protection)
       CommitError: If commit fails (wrapped SQLAlchemyError)
       RollbackError: If rollback fails (wrapped SQLAlchemyError)
    """

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
