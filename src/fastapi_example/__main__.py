import asyncio
import logging
import sys

from .core import load_settings, setup_di_container
from .infrastructure.servers import run_uvicorn_server
from .presentation.api.v1 import init_app_v1
from .presentation.faststream import init_faststream


async def async_main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    settings = load_settings()
    di_container = setup_di_container(settings)
    api = init_app_v1(
        settings.application.v1_api,
        di_container,
    )
    faststream = await init_faststream(di_container)

    async with asyncio.TaskGroup() as tasks:
        tasks.create_task(faststream.run())
        tasks.create_task(run_uvicorn_server(api, settings.infrastructure.server))


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
