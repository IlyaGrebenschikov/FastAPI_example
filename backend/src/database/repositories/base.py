from typing import Type
from abc import abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.common.types import ModelType
from backend.src.database.repositories.crud import CrudRepository


class BaseRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._crud = CrudRepository(self._session, self.model)

    @property
    @abstractmethod
    def model(self) -> Type[ModelType]:
        raise NotImplementedError
