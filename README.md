# FastAPI Example

REST API built with FastAPI, following a layered architecture.

## Stack

- **Python 3.12**, FastAPI, uvicorn
- **PostgreSQL** (asyncpg + SQLAlchemy 2.0)
- **Redis** (refresh tokens, rate limiting)
- **Kafka** via FastStream (email notifications)
- **MailDev** (local SMTP)
- **Dishka** (dependency injection)
- **JWT RS256** (access + refresh tokens)

## Architecture

```
src/fastapi_example/
├── domain/              # entities, value objects
├── application/         # use cases, commands/queries, interfaces
├── infrastructure/      # DB repos, cache, SMTP, Kafka, HTTP clients
├── presentation/        # FastAPI controllers, DTOs, exception handlers
└── core/                # settings, DI container setup
```

## Run locally

### 1. Start infrastructure

```bash
docker compose -f docker-compose.dev.yml up -d
```

### 2. Generate JWT keys

```bash
mkdir -p .certs
openssl genrsa -out .certs/jwt-private.pem 2048
openssl rsa -in .certs/jwt-private.pem -pubout -out .certs/jwt-public.pem
```

### 3. Configure environment

```bash
cp .env_example .env
```

Edit `.env` if needed (defaults work with docker-compose.dev.yml).

### 4. Run migrations

```bash
uv run alembic upgrade head
```

### 5. Start API

```bash
uv run api
```

API is available at `http://localhost:8080`. Docs at `/docs`.

## Run with Docker

```bash
docker compose -f docker-compose.yaml --profile api --profile port-forwarder run --rm migrations
docker compose -f docker-compose.yaml --profile api --profile port-forwarder up api
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/users` | Register user |
| GET | `/users` | Get current user |
| PATCH | `/users` | Update current user |
| DELETE | `/users` | Delete current user |
| POST | `/auth/login/email` | Login by email |
| POST | `/auth/refresh` | Refresh tokens |
| POST | `/auth/logout` | Logout (revoke refresh token) |

## Dev commands

```bash
uv run ruff check src/fastapi_example    # lint
uv run ruff format src/fastapi_example   # format
uv run mypy src/fastapi_example          # typecheck
```
