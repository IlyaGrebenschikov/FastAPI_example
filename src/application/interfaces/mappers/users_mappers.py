from typing import Protocol, TypeVar
from src.domain.entities.user import User
from src.application.dto import CreateUserDTO

PersistenceModel = TypeVar('PersistenceModel')


class IUsersMapper(Protocol[PersistenceModel]):
    def domain_to_persistence(self, domain_user: User) -> PersistenceModel: ...
    def persistence_to_domain(self, persistence_user: PersistenceModel) -> User: ...
    def dto_to_persistence(self, dto: CreateUserDTO) -> PersistenceModel: ...
