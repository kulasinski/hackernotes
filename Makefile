# HackerNotes Makefile

.PHONY: all install dev test lint fmt clean reset

# === Setup ===
install:
	poetry install

deploy:
	poetry build

# === Dev Convenience ===
dev:
	poetry run hn

shell:
	poetry run python

# === Testing ===
test:
	poetry run pytest tests

# === Linting & Formatting ===
lint:
	poetry run ruff check hackernotes

fmt:
	poetry run ruff format hackernotes

# === Maintenance ===
clean:
	rm -rf __pycache__ .pytest_cache .mypy_cache dist

reset: clean
	rm -rf .venv
