from .composition import setup_dependencies, load_settings
from .presentation import init_app
from .presentation.servers import run_uvicorn_server
from .presentation.v1 import init_app_v1

def main() -> None:
    settings = load_settings()
    app = init_app(
        init_app_v1(
            settings.v1_api_settings
        )
    )

    setup_dependencies(app, settings.infrastructure_settings)
    run_uvicorn_server(app, settings.server_settings.uvicorn)


if __name__ == "__main__":
    main()
