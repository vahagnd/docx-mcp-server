# Dont use those yet
server-start-daemon:
	docker compose up -d --remove-orphans
server-start:
	docker compose up --remove-orphans
server-stop:
	docker compose down
server-restart: server-stop server-start

# Init
project-init:
	uv sync
project-init-dev:
	uv sync --extra dev

# Testing
run-tests:
	PYTHONPATH=$(PWD) uv run pytest tests $(filter-out run-tests,$(MAKECMDGOALS))
%:
	@:
