from typing import Protocol, TypeVar
from src.domain.entities.user import User

PersistenceModel = TypeVar('PersistenceModel')


class IUsersRepositoryMapper(Protocol[PersistenceModel]):
    def persistence_to_domain(self, persistence_user: PersistenceModel) -> User: ...
