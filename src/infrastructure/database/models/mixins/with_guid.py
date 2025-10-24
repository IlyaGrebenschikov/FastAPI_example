from uuid import UUID

from sqlalchemy.orm import Mapped


class ModelWithIDMixin:
    id: Mapped[UUID]
