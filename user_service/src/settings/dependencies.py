from fastapi import FastAPI

from user_service.src.database.core.connection import create_engine, create_async_session_maker
from user_service.src.database.markers.database import session_marker
from user_service.src.database.markers.security import jwt_marker, bcrypt_hasher_marker
from user_service.src.core.settings import DatabaseSettings, SecretSettings
from user_service.src.services.security.token_jwt import TokenJWT
from user_service.src.services.security.bcrypt_hasher import BcryptHasher
from user_service.src.services.security.pwd_context import get_pwd_context



def init_dependencies(app: FastAPI, db_settings: DatabaseSettings, secret_settings: SecretSettings) -> None:
    engine = create_engine(db_settings.get_url_obj)
    jwt_token = TokenJWT(secret_settings)
    bcrypt_pwd_context = get_pwd_context(['bcrypt'])
    bcrypt_hasher = BcryptHasher(bcrypt_pwd_context)

    app.dependency_overrides[create_async_session_maker(engine)] = session_marker
    app.dependency_overrides[jwt_token] = jwt_marker
    app.dependency_overrides[bcrypt_hasher] = bcrypt_hasher_marker
