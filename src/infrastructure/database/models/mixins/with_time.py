from datetime import datetime

from sqlalchemy.orm import Mapped


class ModelWithTimeMixin:
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
