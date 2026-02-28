from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

def create_sa_engine(url: str | URL) -> AsyncEngine:
    return create_async_engine(url)


def create_sa_session_factory(
        engine: AsyncEngine,
        autoflush: bool = False,
        expire_on_commit: bool = False
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, autoflush=autoflush, expire_on_commit=expire_on_commit)
