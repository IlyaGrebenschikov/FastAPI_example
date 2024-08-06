from user_service.src.settings.app import init_app, start_app
from user_service.src.core.settings import get_db_settings, get_jwt_settings


def main() -> None:
    db_settings = get_db_settings()
    jwt_settings = get_jwt_settings()
    app = init_app(db_settings, jwt_settings)
    start_app(app)


if __name__ == "__main__":
    main()
