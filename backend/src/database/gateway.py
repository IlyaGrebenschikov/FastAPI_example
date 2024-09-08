from typing import Type

from backend.src.common.interfaces.gateway import BaseGateway
from backend.src.database.core.manager import TransactionManager
from backend.src.database.repositories.user import UserRepository
from backend.src.common.types import RepositoryType


class DBGateway(BaseGateway):
    def __init__(self, manager: TransactionManager) -> None:
        self.manager = manager
        super().__init__(manager)

    def user(self) -> UserRepository:
        return self._init_repo(UserRepository)

    def _init_repo(self, cls: Type[RepositoryType]) -> RepositoryType:
        return cls(self.manager.session)
