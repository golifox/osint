.PHONY: install lint test

install:
	@which pyenv >/dev/null 2>&1 || (echo "pyenv not found. Please install pyenv first."; exit 1)
	@(pyenv versions --bare | grep -q '3.12' ) || pyenv install 3.12
	pyenv local 3.12
	@echo "Please reload your terminal or run 'exec $$SHELL' to re-initialize your shell."
	@echo "Then run 'make init' to continue the installation."

init:
	pip install --upgrade pip
	pip install poetry
	poetry install
	poetry shell

console:
	poetry run python3 .

run:
	poetry run python3 src/desktop/app.py

api:
	poetry run python3 -m src.api

lint:
	@echo "Running code formatter..."
	poetry run black .

test:
	@echo "Running tests..."
	poetry run pytest

migration:
	poetry run alembic revision --autogenerate -m "$(name)"

migrate:
	@echo "Migrating..."
	poetry run alembic upgrade head

seed:
	@echo "Database seeding..."
	poetry run python3 seed.py

prepare:
	poetry run alembic upgrade head
	poetry run python3 seed.py
