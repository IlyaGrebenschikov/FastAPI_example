from .infrastructure import load_infrastructure_settings
from .infrastructure.dependency_injection import setup_infrastructure_dependencies
from .presentation.servers import (
    load_server_settings,
    run_uvicorn_server
    )
from .presentation import init_app
from .presentation.v1 import (
    init_app_v1,
    load_v1_api_settings
    )

def main() -> None:
    server_settings = load_server_settings()
    v1_api_settings = load_v1_api_settings()
    infrastructure_settings = load_infrastructure_settings()
    
    app = init_app(
        init_app_v1(
            v1_api_settings
        )
    )

    setup_infrastructure_dependencies(app, infrastructure_settings)

    run_uvicorn_server(app, server_settings.uvicorn)


if __name__ == "__main__":
    main()
