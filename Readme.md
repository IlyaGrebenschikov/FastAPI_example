# FastAPI Example

Educational FastAPI service following Clean Architecture with Dishka DI, SQLAlchemy 2.0 ORM, JWT auth, Alembic migrations, and monitoring via Loki + Promtail + Grafana. Ready to run in Docker.

## Table of Contents
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Requirements](#requirements)
- [Environment Setup](#environment-setup)
- [JWT Key Generation](#jwt-key-generation)
- [Quick Start](#quick-start)
- [Monitoring](#monitoring)
- [Project Structure](#project-structure)
- [Migrations](#migrations)
- [API Overview](#api-overview)
- [Useful Commands](#useful-commands)
- [DI Container](#di-container)
- [Logging](#logging)

## Tech Stack
- **FastAPI**, Pydantic Settings, **Dishka** (DI)
- **SQLAlchemy 2.0** (async) + asyncpg, **Alembic**
- JWT (RS256), pwdlib[argon2]
- **uvicorn**, **uv** (package/runner)
- **Docker** / Docker Compose
- **Loki** + **Promtail** + **Grafana** (logging)

## Architecture
The project follows Clean Architecture principles:
- `domain` — entities and business rules.
- `application` — DTOs, interfaces, use-case services.
- `infrastructure` — DB adapters, repositories, migrations, settings.
- `presentation` — FastAPI HTTP layer (routes, middlewares, handlers).
- `composition` — app wiring, DI container (Dishka), settings loading.

## Requirements
- Python 3.12+ (Docker image uses 3.13)
- **uv** (https://docs.astral.sh/uv/) or Docker
- Docker Compose v2

## Environment Setup
Create a `.env` file in the project root. Example:

```env
DB_HOST=localhost
DB_PORT=5432
DB_USERNAME=postgres
DB_PASSWORD=postgres
DB_DATABASE=fastapi_example

UVICORN_SERVER_HOST=0.0.0.0
UVICORN_SERVER_PORT=8080

APP_TITLE=FastAPI Example
APP_VERSION=0.1.0
APP_DOCS_URL=/docs
APP_REDOC_URL=/redoc

CORS_ORIGINS=["*"]
CORS_METHODS=["*"]
CORS_HEADERS=["*"]
```

## JWT Key Generation
JWT uses RS256 algorithm. Keys are read from `.certs/jwt-private.pem` and `.certs/jwt-public.pem`.

### Generate Keys (Git Bash on Windows)
1. Navigate to the project root:
   ```bash
   cd /c/path/to/FastAPI_example
   ```

2. Create the `.certs` directory:
   ```bash
   mkdir -p .certs
   ```

3. Generate the private key (RSA 2048-bit):
   ```bash
   openssl genrsa -out .certs/jwt-private.pem 2048
   ```

4. Extract the public key:
   ```bash
   openssl rsa -in .certs/jwt-private.pem -pubout -out .certs/jwt-public.pem
   ```

5. Verify creation:
   ```bash
   ls -la .certs/
   ```

**Note:** Ensure `.certs/` is in `.gitignore` to avoid committing private keys.

### Alternative: Generate Keys (Linux/macOS/WSL)
```bash
mkdir -p .certs
openssl genrsa -out .certs/jwt-private.pem 2048
openssl rsa -in .certs/jwt-private.pem -pubout -out .certs/jwt-public.pem
```

## Quick Start

### Local
```bash
uv sync
uv run alembic upgrade head
uv run api
```
Swagger UI: http://localhost:8080/docs

### Docker
1. Prepare `.env` and JWT keys as above.
2. Run API + Postgres:
   ```bash
   docker compose --profile api up --build
   ```
3. Apply migrations (if not applied automatically):
   ```bash
   docker compose --profile migrations up --build
   ```
4. Stop:
   ```bash
   docker compose --profile api down
   ```

#### Postgres Port Forwarder
The `postgres_port_forwarder` service in Docker Compose allows direct connection to the Postgres database from the host (e.g., for debugging or using external tools like pgAdmin/DBeaver). It forwards port 5432 from the Postgres container to local port 127.0.0.1:5432 using `alpine/socat`.

- **Start:** `docker compose --profile port-forwarder up`
- **Connect:** Use `localhost:5432` in DB tools (use variables from `.env`: `DB_USERNAME`, `DB_PASSWORD`, `DB_DATABASE`).
- **Note:** Only works when the Postgres container is running and healthy. Not for production use — for development only.

## Monitoring
- **Loki** collects logs, **Promtail** reads Docker container logs, **Grafana** for dashboards.
- Start:
  ```bash
  docker compose --profile monitoring up
  ```
- Grafana: http://localhost:3000 (anonymous access enabled, Loki datasource provisioned via `monitoring/grafana/datasourses/grafana-config.yaml`).

## Project Structure
- `src/fastapi_example/presentation/v1` — routes (`/api/v1/users`, `/api/v1/token`), dependencies, exception handlers, CORS.
- `application/services` — user and auth business logic, password hashing.
- `infrastructure/database` — SQLAlchemy models, repositories, transactions, Alembic migrations.
- `composition/di_container.py` — Dishka container wiring.
- `monitoring/*` — Loki/Promtail/Grafana configs.

## Migrations
### Local
```bash
uv run alembic revision -m "message"
uv run alembic upgrade head
```

### Docker
```bash
docker compose --profile migrations up --build
```

## API Overview
- `POST /api/v1/token` — issue JWT via `username`/`password` (OAuth2PasswordRequestForm).
- `POST /api/v1/users` — register user.
- `GET /api/v1/users` — get profile (Bearer token).
- `PATCH /api/v1/users` — update profile.
- `DELETE /api/v1/users` — delete profile.

## Useful Commands
- Run server locally: `uv run api`
- Run format/lint (if configured): `uv run ...`
- Open Swagger: http://localhost:8080/docs

## DI Container
Dishka container registers:
- `DatabaseProvider` (engine, sessions, transactions), `HasherProvider`
- `UsersServiceProvider`, `AuthServiceProvider` (JWT)

## Logging
`logging.basicConfig` sets DEBUG on startup (`__main__.py`). In Docker, container logs are scraped by Promtail and visible in Grafana (Loki).
