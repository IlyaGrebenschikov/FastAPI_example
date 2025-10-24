from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

class BaseRepository(ABC):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self._session = session_factory()
