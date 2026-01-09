from typing import (
    AsyncIterator,
    Protocol,
    Optional,
    Type,
)
from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession

class ITransactionManager(Protocol):
    async def __aexit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_value: Optional[BaseException],
            traceback: Optional[TracebackType],
    ) -> None: ...

    async def __aenter__(self) -> "ITransactionManager": ...

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...

    async def create_transaction(self) -> None: ...

    async def close_transaction(self) -> None: ...

    @property
    def session(self) -> AsyncSession: ...

    def read_only(self) -> AsyncIterator[AsyncSession]: ...
