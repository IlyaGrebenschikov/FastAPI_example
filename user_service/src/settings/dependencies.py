from fastapi import FastAPI

from user_service.src.database.core.connection import create_engine, create_async_session_maker
from user_service.src.database.gateway import DBGateway
from user_service.src.database.core.manager import TransactionManager
from user_service.src.core.settings import DatabaseSettings, JWTSettings
from user_service.src.services.security.token_jwt import TokenJWT
from user_service.src.services.security.bcrypt_hasher import BcryptHasher
from user_service.src.services.security.pwd_context import get_pwd_context
from user_service.src.database.factory import create_database_factory


def init_dependencies(app: FastAPI, db_settings: DatabaseSettings, jwt_settings: JWTSettings) -> None:
    engine = create_engine(db_settings.get_url_obj)
    session = create_async_session_maker(engine)
    db_factory = create_database_factory(TransactionManager, session)

    jwt_token = TokenJWT(jwt_settings)

    bcrypt_pwd_context = get_pwd_context(['bcrypt'])
    bcrypt_hasher = BcryptHasher(bcrypt_pwd_context)

    app.dependency_overrides[DBGateway] = db_factory
    # app.dependency_overrides[TokenJWT] = jwt_token
    # app.dependency_overrides[BcryptHasher] = bcrypt_hasher
