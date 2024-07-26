from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import URL

from user_service.src.app.common.types.database import SessionFactory
from user_service.src.app.core.settings import get_db_settings


def create_engine(url_obj: URL) -> AsyncEngine:
    return create_async_engine(url_obj)


def create_async_session_maker(engine: AsyncEngine) -> SessionFactory:
    return async_sessionmaker(engine, class_=AsyncSession)


async def get_session() -> AsyncSession:
    url_obj = get_db_settings().get_url_obj
    engine = create_engine(url_obj)
    session_maker = create_async_session_maker(engine)

    async with session_maker() as session:
        yield session
