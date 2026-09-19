FROM python:3.13-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/usr/fastapi_example/

WORKDIR /usr/fastapi_example/

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc git \
    && rm -rf /var/lib/apt/lists/

COPY --from=ghcr.io/astral-sh/uv:0.12.5 /uv /usr/local/bin/uv

COPY ./pyproject.toml ./uv.lock ./
RUN uv venv -p 3.13 \
    && uv sync --no-install-project

COPY ./src ./src
COPY ./configs ./configs
COPY ./.certs ./.certs
COPY alembic.ini ./
COPY README.md ./

RUN uv sync
