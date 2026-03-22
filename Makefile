# Dont use those yet
server-docker-start-daemon:
	docker compose up -d --remove-orphans
server-docker-start:
	docker compose up --remove-orphans
server-docker-stop:
	docker compose down
server-docker-restart: server-docker-stop server-docker-start

# Init
project-init:
	uv sync
project-init-dev:
	uv sync --extra dev

# Run server
server-start:
	uv run python -m src.server

# Testing
run-tests:
	PYTHONPATH=$(PWD) uv run --env-file .env pytest tests $(filter-out run-tests,$(MAKECMDGOALS))
%:
	@:
