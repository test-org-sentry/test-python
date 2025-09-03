# Makefile for Sentry Test Python Project

.PHONY: help install install-dev run test lint format clean setup

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies using uv
	uv sync

install-dev: ## Install dependencies with dev tools
	uv sync --extra dev

run: ## Run the application
	uv run python run.py

test-errors: ## Run error testing script
	uv run python scripts/test_errors.py

load-test: ## Run load testing script
	uv run python scripts/load_test.py --threads 5 --errors 10

stress-test: ## Run stress test
	uv run python scripts/load_test.py --stress

simulate: ## Run production simulation for 10 minutes
	uv run python scripts/simulate_production.py --duration 10

test: ## Run pytest
	uv run pytest

lint: ## Run linting tools
	uv run flake8 src/ scripts/
	uv run mypy src/

format: ## Format code with black
	uv run black src/ scripts/

clean: ## Clean up temporary files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/

setup: ## Initial setup (install dependencies and create .env)
	uv sync
	@if [ ! -f .env ]; then cp .env.example .env; echo "Created .env file from .env.example"; fi
	@echo "Setup complete! Run 'make run' to start the application."

# Development commands
dev-install: install-dev ## Install development dependencies
dev-run: ## Run in development mode with auto-reload
	uv run python run.py

# Testing commands
test-basic: ## Run basic error tests
	uv run python scripts/test_errors.py

test-load: ## Run load tests
	uv run python scripts/load_test.py

test-simulate: ## Run production simulation
	uv run python scripts/simulate_production.py

# Utility commands
check: lint test ## Run all checks (lint + test)
update-deps: ## Update dependencies
	uv lock --upgrade

# Docker commands (if you want to add Docker support later)
# docker-build: ## Build Docker image
# 	docker build -t sentry-test-python .

# docker-run: ## Run in Docker container
# 	docker run -p 5000:5000 sentry-test-python
