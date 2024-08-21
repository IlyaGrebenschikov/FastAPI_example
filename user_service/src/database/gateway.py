from typing import Type

from user_service.src.common.interfaces.gateway import BaseGateway
from user_service.src.database.core.manager import TransactionManager
from user_service.src.database.repositories.user import UserRepository
from user_service.src.common.types import RepositoryType


class DBGateway(BaseGateway):
    def __init__(self, manager: TransactionManager) -> None:
        self.manager = manager
        super().__init__(manager)

    def user(self) -> UserRepository:
        return self._init_repo(UserRepository)

    def _init_repo(self, cls: Type[RepositoryType]) -> RepositoryType:
        return cls(self.manager.session)
