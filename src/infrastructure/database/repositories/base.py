from abc import ABC
from typing import TypeVar

SessionFactory = TypeVar('SessionFactory')


class BaseRepository(ABC):
    def __init__(self, session_factory: SessionFactory):
        self._session_factory = session_factory
