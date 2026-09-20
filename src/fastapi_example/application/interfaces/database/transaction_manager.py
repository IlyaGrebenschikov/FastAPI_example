from types import TracebackType
from typing import (
    Protocol,
    TypeVar,
)

SessionT = TypeVar("SessionT")


class ITransactionManager(Protocol[SessionT]):
    async def __aenter__(self) -> "ITransactionManager[SessionT]": ...

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None: ...
