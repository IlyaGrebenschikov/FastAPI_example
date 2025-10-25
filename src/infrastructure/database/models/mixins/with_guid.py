from sqlalchemy.orm import (
    Mapped,
    mapped_column
)
from sqlalchemy.types import UUID


class ModelWithIDMixin:
    id: Mapped[UUID] = mapped_column(
        UUID,
        primary_key=True,
        index=True,
    )
