from sqlalchemy.orm import Mapped

from .base import Base
from .mixins import ModelWithTimeMixin, ModelWithIDMixin

class UserModel(ModelWithIDMixin, ModelWithTimeMixin, Base):
    username: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]

    __tablename__ = "users"
