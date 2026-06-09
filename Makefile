.PHONY: help install dev test lint format typecheck security clean docker-build docker-up pre-commit

help:
	@echo "╔══════════════════════════════════════════════╗"
	@echo "║  AI-Native Cyber Resilience                 ║"
	@echo "╠══════════════════════════════════════════════╣"
	@echo "║  make install     Install production deps    ║"
	@echo "║  make dev         Install dev deps           ║"
	@echo "║  make test        Run all tests              ║"
	@echo "║  make lint        Run ruff linter            ║"
	@echo "║  make format      Run ruff formatter         ║"
	@echo "║  make typecheck   Run mypy type checking     ║"
	@echo "║  make security    Run bandit SAST scan       ║"
	@echo "║  make pre-commit  Run pre-commit hooks       ║"
	@echo "║  make clean       Remove caches and builds   ║"
	@echo "║  make docker-build Build all Docker images   ║"
	@echo "║  make docker-up   Start Docker Compose       ║"
	╚══════════════════════════════════════════════╝

install:
	pip install -e .

dev:
	pip install -e ".[dev,test,ai,docs]"

test:
	pytest --cov=src --cov-report=term-missing --cov-report=xml

lint:
	ruff check src/ tests/

format:
	ruff format src/ tests/

typecheck:
	mypy src/

security:
	bandit -c pyproject.toml -r src/

pre-commit:
	pre-commit run --all-files

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache .mypy_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

docker-build:
	docker compose -f docker/docker-compose.yml build

docker-up:
	docker compose -f docker/docker-compose.yml up -d
