from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


def create_sa_engine(
    url: str | URL,
    pool_size: int = 5,
    max_overflow: int = 10,
    pool_recycle: int = 3600,
) -> AsyncEngine:
    return create_async_engine(
        url,
        pool_size=pool_size,
        max_overflow=max_overflow,
        pool_recycle=pool_recycle,
    )


def create_sa_session_factory(
    engine: AsyncEngine, autoflush: bool = False, expire_on_commit: bool = False
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        engine, autoflush=autoflush, expire_on_commit=expire_on_commit
    )
