BACKEND_SERVICE = backend-service
DB_SERVICE = db-service
NGROK_SERVICE = ngrok

build-all:
	docker compose --env-file ./backend.env --env-file ./ngrok.env build

build-backend:
	docker compose --env-file ./backend.env build $(BACKEND_SERVICE) $(DB_SERVICE)

build-db:
	docker compose --env-file ./backend.env build $(DB_SERVICE)

up-all:
	docker compose --env-file ./backend.env --env-file ./ngrok.env up

up-backend:
	docker compose --env-file ./backend.env up $(BACKEND_SERVICE) $(DB_SERVICE)

up-db:
	docker compose --env-file ./backend.env up $(DB_SERVICE)