BACKEND_SERVICE = backend-service
DB_SERVICE = db-service
NGROK_SERVICE = ngrok
REDIS_SERVICE = redis

build-all:
	docker compose --env-file ./backend.env --env-file ./ngrok.env build

build-backend:
	docker compose --env-file ./backend.env build $(BACKEND_SERVICE) $(DB_SERVICE)

build-db:
	docker compose --env-file ./backend.env build $(DB_SERVICE)

up-all:
	docker compose --env-file ./backend.env --env-file ./ngrok.env up

up-backend:
	docker compose --env-file ./backend.env up $(BACKEND_SERVICE) $(DB_SERVICE) $(REDIS_SERVICE)

up-db:
	docker compose --env-file ./backend.env up $(DB_SERVICE)

up-redis:
	docker compose --env-file ./backend.env up $(REDIS_SERVICE)

stop-all:
	docker stop $(BACKEND_SERVICE) $(DB_SERVICE) $(NGROK_SERVICE)

stop-backend:
	docker stop $(BACKEND_SERVICE) $(DB_SERVICE) $(REDIS_SERVICE)

stop-db:
	docker stop $(DB_SERVICE)

stop-ngrok:
	docker stop $(NGROK_SERVICE)

stop-redis:
	docker stop $(REDIS_SERVICE)

redis-monitor:
	docker exec -it $(REDIS_SERVICE) redis-cli monitor
	