from abc import ABC
from typing import TypeVar

Session = TypeVar("Session")


class BaseRepository(ABC):
    def __init__(self, session: Session):
        self._session = session
