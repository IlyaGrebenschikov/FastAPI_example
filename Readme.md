## FastAPI Example

Educational FastAPI service following Clean Architecture with Dishka DI, SQLAlchemy 2.0 ORM, JWT auth, Alembic migrations, and monitoring via Loki + Promtail + Grafana. Ready to run in Docker.

### Stack
- FastAPI, Pydantic Settings, dishka (DI)
- SQLAlchemy 2.0 (async) + asyncpg, Alembic
- JWT (RS256), pwdlib[argon2]
- uvicorn, uv (package/runner)
- Docker / docker compose
- Loki + Promtail + Grafana (logging)

### Architecture
- `domain` — entities and business rules.
- `application` — DTOs, interfaces, use-case services.
- `infrastructure` — DB adapters, repositories, migrations, settings.
- `presentation` — FastAPI HTTP layer (routes, middlewares, handlers).
- `composition` — app wiring, DI container (Dishka), settings loading.

### Requirements
- Python 3.12+ (Docker image uses 3.13)
- uv (https://docs.astral.sh/uv/) or Docker
- Docker Compose v2

### Environment (.env)
Example:
```
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

### JWT Keys Setup
JWT uses RS256 algorithm. Keys are read from `.certs/jwt-private.pem` and `.certs/jwt-public.pem`.

#### Generate JWT Keys (Git Bash on Windows)
If you're using Git Bash on Windows, follow these steps:

1. Navigate to the project root directory:
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

4. Extract the public key from the private key:
```bash
openssl rsa -in .certs/jwt-private.pem -pubout -out .certs/jwt-public.pem
```

5. Verify the keys were created:
```bash
ls -la .certs/
```

**Note:** Make sure `.certs/` is in your `.gitignore` file to prevent committing private keys to the repository.

#### Alternative: Generate JWT Keys (Linux/macOS/WSL)
```bash
mkdir -p .certs
openssl genrsa -out .certs/jwt-private.pem 2048
openssl rsa -in .certs/jwt-private.pem -pubout -out .certs/jwt-public.pem
```

### Quick start (local)
```
uv sync
uv run alembic upgrade head
uv run api
```
Swagger UI: http://localhost:8080/docs

### Quick start (Docker)
1) Prepare `.env` and JWT keys as above.
2) Run API + Postgres:
```
docker compose --profile api up --build
```
3) Apply migrations (if not already):
```
docker compose --profile migrations up --build
```
4) Stop:
```
docker compose --profile api down
```

### Monitoring
- `loki` collects logs, `promtail` reads Docker logs, `grafana` for dashboards.
- Start:
```
docker compose --profile monitoring up
```
Grafana: http://localhost:3000 (anonymous access enabled, Loki datasource provisioned via `monitoring/grafana/datasourses/grafana-config.yaml`).

### Structure
- `src/fastapi_example/presentation/v1` — routes (`/api/v1/users`, `/api/v1/token`), dependencies, exception handlers, CORS.
- `application/services` — user and auth business logic, password hashing.
- `infrastructure/database` — SQLAlchemy models, repositories, transactions, Alembic migrations.
- `composition/di_container.py` — Dishka container wiring.
- `monitoring/*` — Loki/Promtail/Grafana configs.

### Migrations
Local:
```
uv run alembic revision -m "message"
uv run alembic upgrade head
```
Docker:
```
docker compose --profile migrations up --build
```

### API overview
- `POST /api/v1/token` — issue JWT via `username`/`password` (OAuth2PasswordRequestForm).
- `POST /api/v1/users` — register user.
- `GET /api/v1/users` — get profile (Bearer token).
- `PATCH /api/v1/users` — update profile.
- `DELETE /api/v1/users` — delete profile.

### Handy commands
- Run server locally: `uv run api`
- Run format/lint (if configured): `uv run ...`
- Open Swagger: `http://localhost:8080/docs`

### What’s in DI
Dishka container registers:
- `DatabaseProvider` (engine, sessions, transactions)
- `UsersServiceProvider`, `HasherServiceProvider`, `AuthServiceProvider` (JWT)

### Logging
`logging.basicConfig` sets DEBUG on startup (`__main__.py`). In Docker, container logs are scraped by Promtail and visible in Grafana (Loki).
