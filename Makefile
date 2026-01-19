up:
	if docker network ls --format "{{.Name}}" | grep ai_network; then \
		echo "Network 'ai_network' already exists"; \
	else \
		echo "Creating network 'ai_network'..."; \
		docker network create ai_network; \
	fi

	docker compose build
	docker compose down
	docker compose up -d
	docker exec -it ollama sh -c 'ollama pull "$$AI_MODEL"'
	docker exec -it ollama sh -c 'echo "$$AI_MODEL"'

stop:
	docker compose stop

up-dev:
	@PYTHONPATH=src fastapi dev src/main.py

format:
	uv run ruff check --select I,F401 --fix
	uv run ruff format

down:
	docker compose down
	docker volume prune -a -f

prune:
	make stop
	docker compose down
	docker system prune -a -f
	docker volume prune -a -f
