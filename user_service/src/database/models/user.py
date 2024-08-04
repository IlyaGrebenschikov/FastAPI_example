from sqlalchemy.orm import Mapped, mapped_column

from user_service.src.database.models.base.core import Base
from user_service.src.database.models.base.mixins.with_id import ModelWithIDMixin
from user_service.src.database.models.base.mixins.with_time import ModelWithTimeMixin


class UserModel(ModelWithIDMixin, ModelWithTimeMixin, Base):
    __tablename__ = 'user'

    login: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    is_superuser: Mapped[bool] = mapped_column(nullable=False, default=False)
