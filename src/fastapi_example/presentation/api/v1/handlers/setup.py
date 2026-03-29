from fastapi import FastAPI

from fastapi_example.presentation.api.common.handlers import setup_exception_handlers


def setup_handlers(app: FastAPI) -> None:
    setup_exception_handlers(app)
