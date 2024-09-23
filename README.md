# FastAPI example app

## About project:

### Description:
A simple asynchronous API application that implements CRUD user interaction.

### Stack:

#### Languages:
- `Python`

#### Frameworks:
- `FastAPI`

#### Databases:
- `PostgreSQL`, `Redis`

#### ORM, migrations and drivers for DB:
`Alembic`, `SQLAlchemy`, `AsyncPG`

#### Security:
- `Bcrypt`

#### Containerization:
- `Docker`

#### Development Tools:
- `Ngrok`, `Makefile`

## Setup:
### Env-file:
Rename `.backend_example` to `backend.env` and `.ngrok_example` to `ngrok.env` then set your values.

### Docker:
#### Windows:
`make create-certs-windows` `make build-backend` `make up-all`

#### Unix:
`make create-certs-unix` `make build-backend` `make up-all`

### Remark:
If you don't want to start the `Ngrok` service then use `make up-backend` instead of `make up-all`

### TODO:
- [x] Migrations
- [x] Docker support
- [x] Cache
- [ ] Tests
- [ ] Logging