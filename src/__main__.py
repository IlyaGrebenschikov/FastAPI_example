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
    
    app = init_app(
        init_app_v1(
            v1_api_settings
        )
    )
    
    run_uvicorn_server(app, server_settings.uvicorn)


if __name__ == "__main__":
    main()
