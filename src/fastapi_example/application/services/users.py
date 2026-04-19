import logging

from fastapi_example.application.interfaces.database import ITransactionManager
from fastapi_example.application.interfaces.database.repositories import (
    IUsersRepository,
)
from fastapi_example.application.interfaces.services.mappers import IUsersServiceMapper
from fastapi_example.application.interfaces.security import IHasher
from fastapi_example.application.interfaces.services import IUsersService

log = logging.getLogger(__name__)


class UsersService(IUsersService):
    def __init__(
        self,
        repository: IUsersRepository,
        mapper: IUsersServiceMapper,
        hasher: IHasher,
        transaction_manager: ITransactionManager,
    ):
        self._repository = repository
        self._mapper = mapper
        self._hasher = hasher
        self._transaction_manager = transaction_manager
