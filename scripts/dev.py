#!/usr/bin/env python3
"""
Development utility scripts for Riot Pulse

This script provides common development tasks like linting, formatting,
testing, and code quality checks.

Usage:
    python scripts/dev.py <command>

Available commands:
    lint        - Run linting and type checking
    format      - Format code with ruff
    test        - Run all tests
    test-unit   - Run unit tests only
    test-int    - Run integration tests only
    coverage    - Run tests with coverage report
    clean       - Clean up generated files
    install     - Install development dependencies
    pre-commit  - Set up pre-commit hooks
    check       - Run all quality checks (lint + test)
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: str, cwd: Path | None = None) -> int:
    """Run a shell command and return exit code"""
    print(f"🔧 Running: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd)
    if result.returncode == 0:
        print("✅ Success")
    else:
        print(f"❌ Failed with exit code {result.returncode}")
    return result.returncode


def run_commands(commands: list[str], cwd: Path | None = None) -> int:
    """Run multiple commands and return max exit code"""
    exit_codes = []
    for cmd in commands:
        exit_codes.append(run_command(cmd, cwd))
    return max(exit_codes)


def get_project_root() -> Path:
    """Get the project root directory"""
    return Path(__file__).parent.parent


def lint() -> int:
    """Run linting and type checking"""
    print("🔍 Running code quality checks...")
    commands = [
        "uv run --quiet ruff check .",
        "uv run --quiet ruff format --check .",
        # Note: mypy disabled for gradual typing adoption
        # "uv run --quiet mypy riot_pulse",
    ]
    return run_commands(commands, get_project_root())


def format_code() -> int:
    """Format code with ruff"""
    print("🎨 Formatting code...")
    return run_command("uv run --quiet ruff format .", get_project_root())


def test() -> int:
    """Run all tests"""
    print("🧪 Running all tests...")
    return run_command("uv run --quiet pytest", get_project_root())


def test_unit() -> int:
    """Run unit tests only"""
    print("🧪 Running unit tests...")
    return run_command("uv run --quiet pytest tests/unit/", get_project_root())


def test_integration() -> int:
    """Run integration tests only"""
    print("🧪 Running integration tests...")
    return run_command(
        "uv run --quiet pytest tests/integration/ -m integration", get_project_root()
    )


def coverage() -> int:
    """Run tests with coverage report"""
    print("📊 Running tests with coverage...")
    commands = [
        "uv run --quiet pytest --cov --cov-report=term-missing --cov-report=html",
        "echo '📊 Coverage report generated in htmlcov/index.html'",
    ]
    return run_commands(commands, get_project_root())


def clean() -> int:
    """Clean up generated files"""
    print("🧹 Cleaning up generated files...")
    commands = [
        "rm -rf .pytest_cache",
        "rm -rf .coverage",
        "rm -rf htmlcov",
        "rm -rf .mypy_cache",
        "rm -rf .ruff_cache",
        "find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true",
        "find . -name '*.pyc' -delete",
    ]
    return run_commands(commands, get_project_root())


def install() -> int:
    """Install development dependencies"""
    print("📦 Installing development dependencies...")
    return run_command("uv sync --dev", get_project_root())


def pre_commit_setup() -> int:
    """Set up pre-commit hooks"""
    print("🪝 Setting up pre-commit hooks...")
    commands = [
        "uv run --quiet pre-commit install",
        "uv run --quiet pre-commit run --all-files || true",  # Don't fail on first run
    ]
    return run_commands(commands, get_project_root())


def check() -> int:
    """Run all quality checks (lint + test)"""
    print("🔎 Running comprehensive quality checks...")
    print("=" * 50)

    # Run linting first
    lint_result = lint()
    print("=" * 50)

    # Run tests
    test_result = test()
    print("=" * 50)

    # Summary
    if lint_result == 0 and test_result == 0:
        print("🎉 All checks passed!")
        return 0
    else:
        print("❌ Some checks failed:")
        if lint_result != 0:
            print("  - Linting/type checking failed")
        if test_result != 0:
            print("  - Tests failed")
        return max(lint_result, test_result)


def help_command() -> int:
    """Show help message"""
    print(__doc__)
    return 0


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        help_command()
        sys.exit(1)

    command = sys.argv[1].replace("-", "_")

    # Available commands
    commands = {
        "lint": lint,
        "format": format_code,
        "test": test,
        "test_unit": test_unit,
        "test_int": test_integration,
        "test_integration": test_integration,
        "coverage": coverage,
        "clean": clean,
        "install": install,
        "pre_commit": pre_commit_setup,
        "precommit": pre_commit_setup,
        "check": check,
        "help": help_command,
    }

    if command in commands:
        try:
            sys.exit(commands[command]())
        except KeyboardInterrupt:
            print("\n⏹️  Operation cancelled by user")
            sys.exit(130)
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)
    else:
        print(f"❌ Unknown command: {sys.argv[1]}")
        print("Available commands:", ", ".join(sorted(commands.keys())))
        sys.exit(1)


if __name__ == "__main__":
    main()
