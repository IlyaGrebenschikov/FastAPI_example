FROM python:3.13-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/usr/api/

WORKDIR /usr/api

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl \
    && pip install --upgrade pip \
    && pip install poetry \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi

COPY src ./src

COPY alembic.ini ./