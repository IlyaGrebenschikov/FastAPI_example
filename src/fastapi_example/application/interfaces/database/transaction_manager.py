from types import TracebackType
from typing import (
    Optional,
    Protocol,
    Type,
    TypeVar,
)

from fastapi_example.application.dto import SessionT


class ITransactionManager(Protocol[SessionT]):
    async def __aenter__(self) -> "ITransactionManager[SessionT]": ...

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None: ...
