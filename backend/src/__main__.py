from backend.src.settings.app import init_app, start_app
from backend.src.core.settings import get_db_settings, get_jwt_settings, get_redis_settings


def main() -> None:
    db_settings = get_db_settings()
    jwt_settings = get_jwt_settings()
    redis_settings = get_redis_settings()
    app = init_app(db_settings, jwt_settings, redis_settings)
    start_app(app)


if __name__ == "__main__":
    main()
