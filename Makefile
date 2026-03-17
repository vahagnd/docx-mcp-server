server-start-daemon:
	docker compose up -d --remove-orphans
server-start:
	docker compose up --remove-orphans
server-stop:
	docker compose down
server-restart: server-stop server-start
