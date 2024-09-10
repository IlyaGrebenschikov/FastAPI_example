build:
	docker compose --env-file ./backend.env --env-file ./ngrok.env build

up:
	docker compose --env-file ./backend.env --env-file ./ngrok.env up
