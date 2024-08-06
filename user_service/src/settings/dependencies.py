from fastapi import FastAPI

from user_service.src.database.core.connection import create_engine, create_async_session_maker
from user_service.src.database.markers.database import session_marker
from user_service.src.database.markers.security import jwt_marker
from user_service.src.core.settings import DatabaseSettings, SecretSettings
from user_service.src.services.security.jwt import JWTToken


def init_dependencies(app: FastAPI, db_settings: DatabaseSettings, secret_settings: SecretSettings) -> None:
    engine = create_engine(db_settings.get_url_obj)
    jwt_token = JWTToken(secret_settings)
    app.dependency_overrides[create_async_session_maker(engine)] = session_marker
    app.dependency_overrides[jwt_token] = jwt_marker
