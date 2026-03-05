from typing import (
    Protocol,
    Optional,
    Type,
    TypeVar,
    AsyncContextManager,
)
from types import TracebackType

SessionT = TypeVar("SessionT")


class ITransactionManager(Protocol[SessionT]):
    async def __aexit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_value: Optional[BaseException],
            traceback: Optional[TracebackType],
    ) -> None: ...

    async def __aenter__(self) -> "ITransactionManager[SessionT]": ...

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...

    async def create_transaction(self) -> None: ...

    async def close_transaction(self) -> None: ...

    @property
    def session(self) -> SessionT: ...

    def read_only(self) -> AsyncContextManager[SessionT]: ...
