# FastAPI Example

Production-ready educational FastAPI service implementing **Vertical Slices** + **CQRS** + **Onion Architecture** patterns. Features async SQLAlchemy 2.0, JWT authentication, dependency injection (Dishka), Redis caching/rate limiting, and comprehensive observability stack (Loki + Promtail + Grafana). Dockerized and fully automated.

## Table of Contents
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
  - [Core Principles](#core-principles)
  - [Layered Structure](#layered-structure)
  - [Vertical Slices](#vertical-slices)
  - [CQRS Pattern](#cqrs-pattern)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Environment Setup](#environment-setup)
- [JWT Key Generation](#jwt-key-generation)
- [Quick Start](#quick-start)
- [API Overview](#api-overview)
- [Monitoring & Logging](#monitoring--logging)
- [Rate Limiting](#rate-limiting)
- [Email Verification](#email-verification)
- [Database Migrations](#database-migrations)
- [Dependency Injection](#dependency-injection)
- [Useful Commands](#useful-commands)

## Tech Stack

### Core Framework & Web
- **FastAPI** 0.119+ — Modern async web framework
- **Uvicorn** 0.38+ — ASGI server
- **Pydantic** 2+ — Data validation & settings management

### Database & ORM
- **SQLAlchemy 2.0** — Async ORM with full type hints
- **asyncpg** 0.30+ — High-performance PostgreSQL async driver
- **Alembic** 1.17+ — Database migrations

### Security & Authentication
- **PyJWT** 2.10+ — JWT token handling
- **pwdlib[argon2]** 0.3+ — Password hashing (Argon2)
- **cryptography** 46+ — Cryptographic operations

### Dependency Injection
- **Dishka** 1.7+ — Lightweight, scoped async DI container

### Caching & Rate Limiting
- **Redis** 7.3+ — Distributed cache & rate limiting state

### Observability
- **Loki** — Log aggregation
- **Promtail** — Log shipper
- **Grafana** — Dashboard & visualization

### Development Tools
- **uv** — Ultra-fast Python package manager & runner
- **Ruff** 0.15+ — Fast Python linter & formatter
- **MyPy** 1.19+ — Static type checker
- **Docker** & **Docker Compose** — Containerization

## Architecture

### Core Principles

The project implements three complementary architectural patterns for scalability, maintainability, and testability:

#### **Vertical Slices**
Features are organized as independent, self-contained vertical slices. Each slice (e.g., `users`, `auth`) encapsulates all layers of functionality—from presentation to infrastructure—reducing coupling and enabling independent feature development. Each feature has its own commands/queries and handlers, organized under `application/features/{feature}/{operation}/`.

#### **CQRS (Command Query Responsibility Segregation)**
Requests are split into two types:
- **Commands** — State-changing operations (create, update, delete). Each command is handled by a dedicated handler.
- **Queries** — State-reading operations (get, list). Each query is handled by a dedicated handler.

This separation provides:
- Clear intent in code (command vs. query operations)
- Optimizable read/write paths independently
- Simplified testing and reasoning about side effects

#### **Onion Architecture (Layered)**
The codebase is organized in concentric layers, each with well-defined responsibilities:

```
┌─────────────────────────────────────────┐
│   Presentation (API, Controllers)       │  HTTP endpoints, routing
├─────────────────────────────────────────┤
│   Application (Features, Handlers)      │  Business logic, use cases
├─────────────────────────────────────────┤
│   Domain (Entities, Business Rules)     │  Core entities, invariants
├─────────────────────────────────────────┤
│   Infrastructure (Repositories, DB)     │  External integrations
└─────────────────────────────────────────┘
```

### Layered Structure

#### **1. Domain Layer** (`domain/`)
- **Purpose:** Core business entities and rules (highest level of abstraction).
- **Contents:** Entity dataclasses (`User`), value objects, business constants.
- **Dependencies:** None (pure Python, framework-agnostic).
- **Example:** `User` entity with core properties and domain mixins.

#### **2. Application Layer** (`application/`)
- **Purpose:** Business logic orchestration, use-case implementation via CQRS handlers.
- **Sub-layers:**
  - `features/` — Vertical slices with commands, queries, and handlers
  - `interfaces/` — Protocols for repositories, services, and external contracts
  - `services/` — Domain services (rate limiting, JWT token handling)
  - `exceptions/` — Application-level exceptions
- **Dependencies:** Domain, external interfaces, infrastructure services.
- **Example:** `CreateUserHandler` validates input, checks for duplicates, hashes password, persists via repository.

#### **3. Infrastructure Layer** (`infrastructure/`)
- **Purpose:** External systems, adapters, and concrete implementations.
- **Sub-layers:**
  - `database/` — SQLAlchemy models, repository implementations, migrations, connection pooling
  - `cache/` — Redis client wrapper, rate limiter cache repository
  - `security/` — Password hasher implementations
  - `servers/` — Uvicorn server configuration
  - `di_providers/` — Dishka provider implementations
- **Dependencies:** Domain, application interfaces, external libraries.
- **Example:** `SQLAlchemyUsersRepository` implements `IUsersRepository`, using SQLAlchemy ORM.

#### **4. Presentation Layer** (`presentation/`)
- **Purpose:** HTTP API, request/response handling, routing.
- **Sub-layers:**
  - `api/v1/` — API version management (routes, controllers, DTOs)
  - `controllers/` — Route handlers that instantiate commands/queries and invoke handlers
  - `dto/` — Request/response schemas (Pydantic models)
  - `middlewares/` — HTTP middlewares (CORS, logging, etc.)
  - `handlers/` — Exception handlers, error responses
- **Dependencies:** Application handlers, domain entities.
- **Example:** `POST /api/v1/users` endpoint creates `CreateUserCommand`, invokes handler, returns response DTO.

### CQRS Pattern Implementation

**Commands** handle state-changing operations (create, update, delete). **Queries** handle state-reading operations (get, list). Each is defined as a simple dataclass and executed by a dedicated handler class. Controllers create the appropriate command/query, invoke the handler, and return the response.

## Project Structure

```
fastapi_example/
├── src/fastapi_example/
│   ├── __init__.py
│   ├── __main__.py                  # Application entry point
│   │
│   ├── core/                        # Application setup & composition
│   │   ├── di_container.py          # DI container (Dishka) wiring
│   │   └── settings.py              # Core settings loading
│   │
│   ├── domain/                      # Domain layer (business rules, entities)
│   │   ├── entities/
│   │   │   ├── user.py              # User aggregate root
│   │   │   └── mixins/              # Shared entity mixins (UUID, timestamps)
│   │   └── __init__.py
│   │
│   ├── application/                 # Application layer (use cases, business logic)
│   │   ├── features/                # Vertical slices with CQRS
│   │   │   ├── users/
│   │   │   │   ├── create_user/     # Create user feature (command)
│   │   │   │   │   ├── command.py
│   │   │   │   │   └── handler.py
│   │   │   │   ├── get_user/        # Get user feature (query)
│   │   │   │   │   ├── query.py
│   │   │   │   │   └── handler.py
│   │   │   │   ├── update_user/     # Update user feature (command)
│   │   │   │   │   ├── command.py
│   │   │   │   │   └── handler.py
│   │   │   │   └── delete_user/     # Delete user feature (command)
│   │   │   │       ├── command.py
│   │   │   │       └── handler.py
│   │   │   └── auth/
│   │   │       └── create_access_token/
│   │   │           ├── command.py
│   │   │           └── handler.py
│   │   ├── interfaces/              # Protocols (contracts for external dependencies)
│   │   │   ├── database/            # Repository & transaction manager interfaces
│   │   │   │   ├── repositories/
│   │   │   │   │   ├── users.py    # IUsersRepository protocol
│   │   │   │   │   └── mappers/    # Data mappers (domain ↔ persistence)
│   │   │   │   └── transaction_manager.py
│   │   │   ├── services/            # Service interfaces
│   │   │   │   ├── rate_limiter.py
│   │   │   │   └── token_jwt.py
│   │   │   ├── security/
│   │   │   │   └── hasher.py       # IHasher protocol
│   │   │   ├── cache/
│   │   │   └── http_clients/
│   │   │       └── email_verifier.py # IEmailVerifier protocol
│   │   ├── services/                # Domain services
│   │   │   ├── rate_limiter.py
│   │   │   └── token_jwt.py
│   │   ├── di_providers/            # DI providers for features
│   │   │   ├── features/            # Feature handlers registration
│   │   │   │   ├── users.py
│   │   │   │   └── auth.py
│   │   │   └── services/            # Service providers
│   │   ├── exceptions/
│   │   │   └── http_exceptions.py  # Application exceptions
│   │   ├── settings.py              # Application settings
│   │   └── __init__.py
│   │
│   ├── infrastructure/              # Infrastructure layer (DB, cache, external services)
│   │   ├── database/
│   │   │   ├── connection.py        # SQLAlchemy engine/session factory
│   │   │   ├── transaction_manager.py  # Async transaction management
│   │   │   ├── exceptions.py
│   │   │   ├── models/              # SQLAlchemy models (ORM)
│   │   │   │   ├── base.py          # Base model with common fields
│   │   │   │   ├── user.py          # User model
│   │   │   │   └── mixins/          # Model mixins
│   │   │   ├── repositories/        # Repository implementations
│   │   │   │   ├── users.py         # SQLAlchemyUsersRepository
│   │   │   │   └── mappers/         # Mappers: ORM model → domain entity
│   │   │   └── migrations/          # Alembic migration scripts
│   │   │       ├── env.py
│   │   │       ├── script.py.mako
│   │   │       └── versions/        # Migration version files
│   │   ├── cache/
│   │   │   ├── connection.py        # Redis client creation
│   │   │   └── repositories/
│   │   │       └── rate_limiter.py  # Redis rate limiter repository
│   │   ├── security/
│   │   │   └── argon_hasher.py      # Argon2 hasher implementation
│   │   ├── http_clients/
│   │   │   └── email_verifier.py    # AbstractAPI email verification client
│   │   ├── servers/
│   │   │   └── uvicorn_server.py    # Uvicorn server configuration
│   │   ├── di_providers/            # DI providers for infrastructure
│   │   │   ├── database.py
│   │   │   ├── cache.py
│   │   │   ├── hasher.py
│   │   │   ├── http_clients.py
│   │   │   └── mappers.py
│   │   ├── settings.py              # Infrastructure settings
│   │   └── __init__.py
│   │
│   └── presentation/                # Presentation layer (HTTP API)
│       └── api/
│           ├── common/
│           │   ├── docs.py          # API documentation schemas
│           │   ├── handlers/        # Global exception handlers
│           │   └── middlewares/     # Global middlewares (CORS, logging)
│           └── v1/                  # API version 1
│               ├── __init__.py
│               ├── setup.py         # API initialization
│               ├── controllers/     # Route handlers
│               │   ├── users.py    # User routes
│               │   └── auth.py     # Auth routes
│               ├── dto/             # Request/Response schemas
│               │   └── ...         # Pydantic models
│               ├── dependencies.py  # Route dependencies
│               ├── handlers/        # Exception handlers
│               ├── middlewares/     # V1 middlewares
│               └── setup_controllers.py
│
├── monitoring/                      # Observability configuration
│   ├── grafana/
│   │   └── datasourses/
│   │       └── grafana-config.yaml  # Grafana provisioning
│   ├── loki/
│   │   └── loki-config.yaml         # Loki log aggregation config
│   └── promtail/
│       └── promtail-config.yaml     # Promtail log shipper config
│
├── pyproject.toml                   # Project metadata & dependencies
├── Dockerfile                       # Application container
├── docker-compose.yaml              # Multi-container orchestration
└── alembic.ini                      # Alembic configuration
```

### Key Files Explained

| File | Purpose |
|------|---------|
| `__main__.py` | Entry point: loads settings, initializes DI container, creates app, runs server |
| `core/di_container.py` | Wires all providers into Dishka async container |
| `application/features/*/handler.py` | Command/Query handlers—orchestrate business logic, use repositories & services |
| `infrastructure/database/repositories/*.py` | Repository implementations—query builders, ORM interactions |
| `presentation/api/v1/controllers/*.py` | Route handlers—accept HTTP requests, delegate to handlers, return responses |
| `domain/entities/*.py` | Business entities—pure dataclasses with no framework dependencies |
## Requirements

- **Python 3.12+** (Docker image uses 3.13 for optimal async performance)
- **uv** (https://docs.astral.sh/uv/) — For local development
- **Docker** & **Docker Compose v2** — For containerized setup
- **PostgreSQL 15+** — Managed via Docker Compose
- **Redis 7.3+** — Managed via Docker Compose

## Environment Setup

Create a `.env` file in the project root with the following variables:

```env
# Database
DB_HOST=localhost
DB_PORT=5432
DB_USERNAME=postgres
DB_PASSWORD=postgres
DB_DATABASE=fastapi_example

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your_secure_redis_password

# API Server
UVICORN_SERVER_HOST=0.0.0.0
UVICORN_SERVER_PORT=8080

# Application
APP_TITLE=FastAPI Example
APP_VERSION=0.1.0
APP_DOCS_URL=/docs
APP_REDOC_URL=/redoc

# CORS
CORS_ORIGINS=["*"]
CORS_METHODS=["*"]
CORS_HEADERS=["*"]

# JWT (RSA-2048 keys in .certs/ directory)
JWT_ALGORITHM=RS256
JWT_EXPIRATION_HOURS=24

# Email Verification (AbstractAPI)
EMAIL_VERIFIER_API_KEY=your_abstractapi_key
```

**Security Note:** In production, restrict `CORS_ORIGINS` to trusted domains and use secure, environment-specific values for `REDIS_PASSWORD`.

## JWT Key Generation

The application uses **RS256** (RSA Signature with SHA-256) for JWT token signing—asymmetric cryptography where the private key signs tokens and the public key verifies them.

### Generate Keys Locally

**On Linux/macOS/WSL:**
```bash
mkdir -p .certs
openssl genrsa -out .certs/jwt-private.pem 2048
openssl rsa -in .certs/jwt-private.pem -pubout -out .certs/jwt-public.pem
ls -la .certs/
```

**On Windows (Git Bash):**
```bash
mkdir -p .certs
cd .certs
openssl genrsa -out jwt-private.pem 2048
openssl rsa -in jwt-private.pem -pubout -out jwt-public.pem
cd ..
```

### Verify Keys
```bash
# Check private key
openssl rsa -in .certs/jwt-private.pem -text -noout

# Check public key
openssl rsa -in .certs/jwt-public.pem -pubin -text -noout
```

### Security Notes
- **Never commit** `.certs/` directory to version control. Ensure it's in `.gitignore`.
- For production, store keys in a secrets manager (HashiCorp Vault, AWS Secrets Manager, etc.).
- Rotate keys periodically in production environments.

## Quick Start

### Local Development (using `uv`)

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Set up environment:**
   - Copy the `.env.example` or create `.env` (see [Environment Setup](#environment-setup))
   - Generate JWT keys (see [JWT Key Generation](#jwt-key-generation))

3. **Start PostgreSQL & Redis (in separate terminals or Docker):**
   ```bash
   docker compose --profile dev up
   ```

4. **Apply migrations:**
   ```bash
   uv run alembic upgrade head
   ```

5. **Run the application:**
   ```bash
   uv run api
   ```

6. **Access API:**
   - Swagger UI: http://localhost:8080/docs
   - ReDoc: http://localhost:8080/redoc
   - API Root: http://localhost:8080

### Docker Setup

**Build and run the full stack (API + PostgreSQL + Redis):**
```bash
# Start with API profile
docker compose --profile api up --build

# In another terminal, apply migrations (if not auto-applied)
docker compose --profile migrations run --rm migrations
```

**Stop containers:**
```bash
docker compose --profile api down
```

**Access services:**
- API: http://localhost:8080/docs
- PostgreSQL: `localhost:5432` (forward port with `--profile port-forwarder`)
- Redis: `localhost:6379` (forward port with `--profile port-forwarder`)

### Docker Compose Profiles

| Profile | Purpose | Services |
|---------|---------|----------|
| `api` | Run API + database | api, postgres, redis |
| `migrations` | Database migrations | migrations, postgres |
| `port-forwarder` | Access database/cache locally | postgres_port_forwarder, redis_port_forwarder |
| `monitoring` | Observability stack | loki, promtail, grafana |

**Example: Start API with port forwarding for debugging:**
```bash
docker compose --profile api --profile port-forwarder up
```

## API Overview

### Endpoints

| Method | Path | Auth | Rate Limit | Description |
|--------|------|------|-----------|-------------|
| `POST` | `/api/v1/token/access` | — | 100/min (IP) | Issue JWT token |
| `POST` | `/api/v1/users` | — | 100/min (IP) | Register new user |
| `GET` | `/api/v1/users` | Bearer token | 100/min (IP), 20/min (user) | Get user profile |
| `PATCH` | `/api/v1/users` | Bearer token | 100/min (IP), 20/min (user) | Update user profile |
| `DELETE` | `/api/v1/users` | Bearer token | 100/min (IP), 20/min (user) | Delete user account |

### Authentication

Register with username/email/password, then login to receive a JWT token. Include the token in subsequent requests via the `Authorization: Bearer {token}` header.

### Response Format

**Success:** Returns user object with `id`, `username`, `email`, `created_at`, `updated_at`.  
**Error:** Returns JSON with error details and appropriate HTTP status code (400, 401, 404, 409, 429, etc.).

## Monitoring & Logging

The project integrates **Loki** (log aggregation), **Promtail** (log shipper), and **Grafana** (visualization) for comprehensive observability.

**Start monitoring stack:**
```bash
docker compose --profile monitoring up
```

**Access Grafana:** http://localhost:3000 (anonymous access enabled, Loki datasource pre-configured)

## Rate Limiting

The project implements a **distributed rate limiter** using Redis with a sliding window algorithm.

**How it works:** Tracks request timestamps per identifier (IP or user ID) in Redis sorted sets. When limit is exceeded, returns HTTP 429 (Too Many Requests).

**Current limits:** All user & auth endpoints enforce 100 requests/minute per IP and 20 requests/minute per authenticated user.

**Customization:** Modify limits in controller files under `presentation/api/v1/controllers/`.

## Email Verification

The application integrates **AbstractAPI Email Reputation** service to validate email addresses during user registration, preventing invalid or disposable email signups.

### How It Works

The `AbstractApiEmailVerifier` client connects to the AbstractAPI service to verify emails across three dimensions:
- **Format validity** — Checks if email follows RFC standards
- **Deliverability** — Verifies the domain accepts mail and the mailbox exists
- **Disposability** — Detects temporary/disposable email services (e.g., 10minutemail.com)

The verifier runs **before** user data is persisted, failing fast with appropriate error messages.

### Setup

1. **Get API key:** Create a free account at [AbstractAPI](https://app.abstractapi.com/) and copy your email reputation API key.

2. **Configure environment:**
   ```env
   EMAIL_VERIFIER_API_KEY=sk_test_YOUR_KEY_HERE
   ```

### How It's Used

During user registration (`POST /api/v1/users`), the `CreateUserHandler` validates the email against three criteria: format validity, deliverability, and disposability. The verifier integrates seamlessly into the registration flow, rejecting invalid emails before user data is persisted.

### Error Handling

The verifier gracefully handles transient failures:
- **Timeout (>5s)** — Returns deliverability=False, user sees "Email verification service unavailable"
- **HTTP 401** — API key invalid, logs error, returns HTTP 503 ServiceUnavailable
- **HTTP 5xx** — Server errors, returns HTTP 503 ServiceUnavailable
- **Network errors** — Returns deliverability=False, defers to backend validation
- **Invalid JSON response** — Logs exception, returns deliverability=False

**Best practice:** The service is non-blocking; temporary failures don't prevent signup attempts but encourage users to provide valid, deliverable addresses.

### Architecture

The email verifier follows **Interface Segregation** and **Dependency Inversion** principles:

- **Interface** (`IEmailVerifier` in `application/interfaces/http_clients/`) — Defines the contract
- **Implementation** (`AbstractApiEmailVerifier` in `infrastructure/http_clients/`) — Concrete adapter to AbstractAPI
- **DI Registration** (`HTTPClientsProvider` in `infrastructure/di_providers/`) — Scoped as APP-lifetime singleton

This design allows swapping AbstractAPI for another provider (Sendgrid, Mailbox Layer, etc.) without changing application logic.

## Database Migrations

Alembic manages schema changes. Migrations are version-controlled in `alembic/versions/`.

**Common commands:**
- Create migration: `uv run alembic revision --autogenerate -m "description"`
- Apply: `uv run alembic upgrade head`
- Rollback: `uv run alembic downgrade -1`
- Docker: `docker compose --profile migrations up --build`

**Best practices:** Always review auto-generated migrations, test locally, keep migrations reversible.

## Dependency Injection

The project uses **Dishka** for asynchronous, scoped dependency injection. All dependencies are wired in a single container (`core/di_container.py`), eliminating tight coupling.

**How it works:**
- **Providers** register dependencies with scope (APP, REQUEST, TRANSIENT)
- **Handlers** declare needed dependencies via type hints
- **Controllers** inject handlers via `FromDishka[HandlerType]`
- **Dishka** resolves and manages lifecycles automatically

**Scope types:**
- `APP` — Application lifetime (DB engines, Redis clients)
- `REQUEST` — Per HTTP request (handlers, repositories)
- `TRANSIENT` — New instance each time (DTOs, lightweight services)

## Useful Commands

**Local Development:**
```bash
uv sync                                    # Install dependencies
uv run api                                 # Run application
uv run ruff check src/ && uv run mypy src/ # Lint & type check
uv run alembic upgrade head                # Apply migrations
```

**Docker:**
```bash
docker compose --profile api up --build              # Start API stack
docker compose --profile monitoring up               # Start monitoring
docker compose --profile api --profile port-forwarder up  # Debug mode
docker compose logs -f api                 # View logs
docker compose down                        # Stop all
```

**Testing API:**
- Swagger UI: http://localhost:8080/docs
- ReDoc: http://localhost:8080/redoc

---

## Contributing

When adding new features, follow the vertical slice pattern:

1. Create feature folder under `application/features/{feature}/{operation}/`
2. Define command or query (dataclass)
3. Implement handler to orchestrate business logic
4. Register handler in DI container
5. Create controller route in `presentation/api/v1/controllers/`
6. Test end-to-end flow

---

## License

This project is provided as an educational example.
