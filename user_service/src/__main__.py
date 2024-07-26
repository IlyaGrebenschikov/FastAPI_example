import uvicorn
from fastapi import FastAPI

from user_service.src.settings.app import create_app


def init_app(app: FastAPI) -> None:
    uvicorn.run(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    app = create_app()
    init_app(app)
