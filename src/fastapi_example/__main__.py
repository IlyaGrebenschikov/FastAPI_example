import logging
import sys

from .core import load_settings, setup_di_container
from .infrastructure.servers import run_uvicorn_server
from .presentation import init_app
from .presentation.v1 import init_app_v1


def main() -> None:
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    settings = load_settings()
    di_container = setup_di_container(settings)
    app = init_app(
        init_app_v1(
            settings.presentation.v1_api,
            di_container,
        )
    )

    run_uvicorn_server(app, settings.infrastructure.server)


if __name__ == "__main__":
    main()
