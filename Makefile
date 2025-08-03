.PHONY: help install lint format test test-unit test-integration coverage clean pre-commit check dev-setup

# Default target
help:
	@echo "Riot Pulse Development Commands"
	@echo "==============================="
	@echo ""
	@echo "Setup:"
	@echo "  install      Install development dependencies"
	@echo "  dev-setup    Full development environment setup"
	@echo "  pre-commit   Set up pre-commit hooks"
	@echo ""
	@echo "Code Quality:"
	@echo "  lint         Run linting and type checking"
	@echo "  format       Format code with ruff"
	@echo "  check        Run all quality checks (lint + test)"
	@echo ""
	@echo "Testing:"
	@echo "  test         Run all tests"
	@echo "  test-unit    Run unit tests only"
	@echo "  test-int     Run integration tests only"
	@echo "  coverage     Run tests with coverage report"
	@echo ""
	@echo "Maintenance:"
	@echo "  clean        Clean up generated files"
	@echo ""
	@echo "For more details, see: python scripts/dev.py help"

# Setup commands
install:
	uv sync --dev

dev-setup: install pre-commit
	@echo "🎉 Development environment setup complete!"

pre-commit:
	uv run python scripts/dev.py pre-commit

# Code quality
lint:
	uv run python scripts/dev.py lint

format:
	uv run python scripts/dev.py format

check:
	uv run python scripts/dev.py check

# Testing
test:
	uv run python scripts/dev.py test

test-unit:
	uv run python scripts/dev.py test-unit

test-int:
	uv run python scripts/dev.py test-int

test-integration:
	uv run python scripts/dev.py test-integration

coverage:
	uv run python scripts/dev.py coverage

# Maintenance
clean:
	uv run python scripts/dev.py clean