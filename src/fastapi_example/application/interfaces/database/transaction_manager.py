from types import TracebackType
from typing import (
    Optional,
    Protocol,
    Type,
    TypeVar,
)

SessionT = TypeVar("SessionT")


class ITransactionManager(Protocol[SessionT]):
    async def __aenter__(self) -> "ITransactionManager[SessionT]": ...

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None: ...
