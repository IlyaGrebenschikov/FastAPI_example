from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import ModelWithTimeMixin, ModelWithIDMixin

class UserModel(ModelWithIDMixin, ModelWithTimeMixin, Base):
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(Text, nullable=False)

    __tablename__ = "users"
