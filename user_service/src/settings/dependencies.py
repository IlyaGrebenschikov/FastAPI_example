from fastapi import FastAPI, Depends

from user_service.src.database.core.connection import create_engine, create_async_session_maker
from user_service.src.database.markers.database import session_marker, engine_marker
from user_service.src.core.settings import DatabaseSettings


def init_dependencies(app: FastAPI, db_settings: DatabaseSettings) -> None:
    app.dependency_overrides[create_engine(db_settings.get_url_obj)] = engine_marker
    app.dependency_overrides[create_async_session_maker(Depends(engine_marker))] = session_marker
