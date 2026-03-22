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
- [Rate Limiting](#rate-limiting)
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
- **Redis** (caching, rate limiting)
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

REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password

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

#### Redis Port Forwarder
The `redis_port_forwarder` service forwards port 6379 from the Redis container to local port 127.0.0.1:6379 using `alpine/socat`. Useful for debugging or connecting external Redis clients (e.g., RedisInsight, another CLI).

- **Start:** `docker compose --profile port-forwarder up`
- **Connect:** Use `localhost:6379` with password from `.env` (`REDIS_PASSWORD`).
- **Note:** Only works when the Redis container is running and healthy. Not for production use — for development only.

## Monitoring
- **Loki** collects logs, **Promtail** reads Docker container logs, **Grafana** for dashboards.
- Start:
  ```bash
  docker compose --profile monitoring up
  ```
- Grafana: http://localhost:3000 (anonymous access enabled, Loki datasource provisioned via `monitoring/grafana/datasourses/grafana-config.yaml`).

## Rate Limiting
The project includes a custom rate limiter powered by **Redis**. It uses a sliding window algorithm to track request counts per identifier (e.g., IP address, user ID) and endpoint path.

### How It Works
- Each request is tracked with a unique timestamp-based key in Redis (sorted set).
- Old entries outside the time window are automatically cleaned up.
- If the request count exceeds the configured limit within the window, a `429 Too Many Requests` error is raised.

### Implementation Details
- **Service:** `RateLimiterService` — checks if the request limit is exceeded.
- **Repository:** `RateLimiterCacheRepository` — interacts with Redis using `redis.asyncio`.
- **Algorithm:** Sliding window with Redis sorted sets (`ZADD`, `ZREMRANGEBYSCORE`, `ZCARD`).

### Usage in Endpoints
Rate limiting is applied to all user-related endpoints (`/api/v1/users/*`) and authentication (`/api/v1/token`). Two levels of limits are enforced:
1. **IP-based limit** — e.g., 100 requests per minute per IP.
2. **User-based limit** — e.g., 20 requests per minute per authenticated user.

Example from `users.py`:
```python
await rate_limiter_service.check(f"ip:{request.client.host}", request.url.path, limit=100, window=60)
await rate_limiter_service.check(f"user:{user_id}", request.url.path, limit=20, window=60)
```

### Configuration
Rate limits are configured per endpoint. The `check` method accepts:
- `identifier` — unique key (e.g., `ip:192.168.1.1`, `user:123`).
- `path` — endpoint path (e.g., `/api/v1/users`).
- `limit` — maximum requests allowed in the window.
- `window` — time window in seconds.

## Project Structure
- `src/fastapi_example/presentation/v1` — routes (`/api/v1/users`, `/api/v1/token`), dependencies, exception handlers, CORS.
- `src/fastapi_example/application/services` — user, auth business logic, password hashing, rate limiting.
- `src/fastapi_example/application/interfaces` — protocol interfaces for services and repositories.
- `src/fastapi_example/infrastructure/database` — SQLAlchemy models, repositories, transactions, Alembic migrations.
- `src/fastapi_example/infrastructure/cache` — Redis connection, repositories (rate limiter).
- `src/fastapi_example/core/di_container.py` — Dishka container wiring.
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
- `DatabaseProvider` (engine, sessions, transactions)
- `CacheProvider` (Redis client)
- `HasherProvider`
- `MappersProvider`
- `RepositoriesProvider`
- `UsersServiceProvider`, `AuthServiceProvider` (JWT)
- `RateLimiterServiceProvider` (custom rate limiting service)

## Logging
`logging.basicConfig` sets DEBUG on startup (`__main__.py`). In Docker, container logs are scraped by Promtail and visible in Grafana (Loki).
