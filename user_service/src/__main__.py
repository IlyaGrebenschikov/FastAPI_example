from user_service.src.settings.app import init_app, start_app
from user_service.src.core.settings import get_db_settings


def main() -> None:
    db_settings = get_db_settings()
    app = init_app(db_settings)
    start_app(app)


if __name__ == "__main__":
    main()
