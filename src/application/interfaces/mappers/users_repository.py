from typing import Protocol, TypeVar
from src.domain.entities.user import User

PersistenceModel = TypeVar('PersistenceModel')


class IUsersRepositoryMapper(Protocol[PersistenceModel]):
    def domain_to_persistence(self, domain_user: User) -> PersistenceModel: ...
    def persistence_to_domain(self, persistence_user: PersistenceModel) -> User: ...
