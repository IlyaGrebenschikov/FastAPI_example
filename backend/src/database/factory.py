from typing import Callable, Type

from backend.src.database.core.manager import TransactionManager
from backend.src.database.gateway import DBGateway
from backend.src.common.types import SessionFactoryType


def create_database_factory(
    manager: Type[TransactionManager], session_factory: SessionFactoryType
) -> Callable[[], DBGateway]:
    def _create() -> DBGateway:
        return DBGateway(manager(session_factory()))

    return _create
