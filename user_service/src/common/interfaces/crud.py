from abc import ABC, abstractmethod
from typing import Generic, Any, Optional, Sequence, Mapping

from user_service.src.common.types import ModelType


class AbstractCrudRepository(ABC):
    def __init__(self, model: Generic[ModelType]) -> None:
        self.model = model

    @abstractmethod
    async def select(self, *args: Any) -> Optional[ModelType]:
        raise NotImplemented

    @abstractmethod
    async def select_many(
            self,
            *args: Any,
            offset: Optional[int] = None,
            limit: Optional[int] = None
    ) -> Optional[Sequence[ModelType]]:
        raise NotImplemented

    @abstractmethod
    async def insert(self, **kwargs: Mapping[str, Any]) -> Optional[ModelType]:
        raise NotImplemented

    @abstractmethod
    async def insert_many(self, **kwargs: Sequence[Mapping[str, Any]]) -> Optional[Sequence[ModelType]]:
        raise NotImplemented

    @abstractmethod
    async def update(self, *args, **kwargs: Mapping[str, Any]) -> Optional[ModelType]:
        raise NotImplemented

    @abstractmethod
    async def update_many(self, *args, **kwargs: Sequence[Mapping[str, Any]]) -> Optional[Sequence[ModelType]]:
        raise NotImplemented

    @abstractmethod
    async def delete(self, *args: Any) -> Optional[ModelType]:
        raise NotImplemented
