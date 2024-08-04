from typing import Annotated

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import URL

from user_service.src.common.types import SessionFactory
from user_service.src.database.markers.database import session_marker


def create_engine(url_obj: URL) -> AsyncEngine:
    return create_async_engine(url_obj)


def create_async_session_maker(engine: AsyncEngine) -> SessionFactory:
    return async_sessionmaker(engine, class_=AsyncSession)


async def get_async_session(
        session_maker: Annotated[SessionFactory, session_marker],
) -> AsyncSession:
    async with session_maker() as session:
        yield session
