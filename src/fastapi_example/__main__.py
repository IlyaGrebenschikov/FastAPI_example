import asyncio
import logging
import sys

from .core import load_configs, load_settings, setup_di_container
from .infrastructure.server import run_uvicorn_server
from .presentation.api import init_api
from .presentation.faststream import init_faststream


async def async_main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    settings = load_settings()
    configs = load_configs()
    di_container = setup_di_container(settings)
    api = init_api(
        app_config=configs.app,
        cors_config=configs.cors,
        di_container=di_container,
    )
    faststream = await init_faststream(di_container)
    async with asyncio.TaskGroup() as tg:
        tg.create_task(run_uvicorn_server(api, settings.server))
        tg.create_task(faststream.start())


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
