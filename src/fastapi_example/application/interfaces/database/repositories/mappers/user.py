from typing import Protocol, TypeVar

from fastapi_example.domain.entities.user import User

PersistenceModel = TypeVar("PersistenceModel", contravariant=True)


class IUsersRepositoryMapper(Protocol[PersistenceModel]):
    def persistence_to_domain(self, persistence_user: PersistenceModel) -> User: ...
