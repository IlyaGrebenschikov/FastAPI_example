FROM python:3.13-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/usr/api/

WORKDIR /usr/api

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc git \
    && rm -rf /var/lib/apt/lists/

RUN pip install --no-cache-dir uv

COPY ./pyproject.toml ./uv.lock ./
RUN uv venv -p 3.13 \
    && uv sync --all-extras --no-install-project
COPY ./src ./src
RUN uv sync --all-extras --no-editable

COPY alembic.ini ./

CMD ["uv", "run", "api"]
