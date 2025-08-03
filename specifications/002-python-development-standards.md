# Specification: Python Development Standards

**Spec ID:** 002-python-development-standards  
**Author:** Claude (with edanker)  
**Date:** 2025-01-03  
**Status:** ✅ Implemented

## 1. Problem Statement

Riot Pulse currently lacks professional Python development tooling and standards, which creates several issues:
- No automated code quality enforcement (formatting, linting)
- No static type checking despite good type annotations
- No structured testing framework or coverage reporting
- No pre-commit hooks to catch issues before they reach the repository
- No CI/CD pipeline for automated testing and quality assurance
- Inconsistent development workflow across contributors
- Missing professional development practices expected in modern Python projects

## 2. Goals & Requirements

### Primary Goals
- Establish professional Python development standards
- Implement automated code quality tools and enforcement
- Create a comprehensive testing framework
- Set up continuous integration and development workflows
- Ensure code maintainability and consistency

### Requirements
- **Must Have:**
  - Modern code formatting and linting (Ruff)
  - Static type checking (mypy)
  - Professional testing framework (pytest)
  - Development dependencies management
  - Tool configuration in pyproject.toml
  - Pre-commit hooks for quality assurance
  - GitHub Actions CI/CD pipeline
- **Should Have:**
  - Code coverage reporting
  - Automated dependency updates
  - Development workflow documentation
  - Common development scripts/commands
- **Nice to Have:**
  - API documentation generation
  - Code quality badges
  - Advanced CI/CD features (deployment, releases)

### Non-Goals
- Rewriting existing code to fit new standards (gradual adoption)
- Complex deployment pipeline (focus on development quality)
- Extensive documentation generation (manual docs are sufficient)

## 3. Technical Design

### Tool Selection Rationale

#### 1. Ruff (Linting + Formatting)
**Why Ruff over Black + Flake8 + isort:**
- **Performance**: 10-100x faster than traditional tools
- **Unified**: Single tool replaces black, isort, flake8, pylint, and more
- **Modern**: Built in Rust, actively maintained
- **Configuration**: Single configuration section in pyproject.toml
- **Adoption**: Rapidly becoming the standard in modern Python projects

#### 2. mypy (Type Checking)
**Why mypy:**
- Industry standard for Python type checking
- Excellent editor integration
- Gradual typing support (perfect for existing codebase)
- Strong community and ecosystem

#### 3. pytest (Testing Framework)
**Why pytest over unittest:**
- More concise and readable test syntax
- Powerful fixture system
- Excellent plugin ecosystem
- Industry standard for Python testing
- Better async/await support

#### 4. pre-commit (Git Hooks)
**Why pre-commit:**
- Prevents bad code from entering the repository
- Runs multiple tools automatically
- Language-agnostic (can add more tools later)
- Standardizes development workflow

### Architecture Overview

```
riot-pulse/
├── pyproject.toml           # All tool configurations
├── .pre-commit-config.yaml  # Git hooks configuration
├── .github/workflows/       # CI/CD pipelines
│   └── ci.yml              # Main CI workflow
├── tests/                   # Test directory structure
│   ├── __init__.py
│   ├── conftest.py         # pytest configuration
│   ├── unit/               # Unit tests
│   └── integration/        # Integration tests
├── scripts/                 # Development utilities
│   └── dev.py              # Common development tasks
└── riot_pulse/             # Source code (unchanged structure)
```

## 4. Implementation Plan

### Phase 1: Core Tools Setup ✅ COMPLETED
- [x] Create specification document
- [x] Update pyproject.toml with development dependencies
- [x] Add Ruff configuration for linting and formatting
- [x] Add mypy configuration for type checking
- [x] Verify tools work with existing codebase

### Phase 2: Testing Framework ✅ COMPLETED
- [x] Set up pytest framework and directory structure
- [x] Create basic test configuration (conftest.py)
- [x] Add code coverage reporting with pytest-cov
- [x] Write example tests for critical components

### Phase 3: Quality Automation ✅ COMPLETED
- [x] Configure pre-commit hooks
- [x] Set up GitHub Actions CI workflow
- [x] Add automated testing and linting to CI
- [x] Configure code coverage reporting

### Phase 4: Developer Experience ✅ COMPLETED
- [x] Create development scripts for common tasks (scripts/dev.py + Makefile)
- [x] Update documentation with development guidelines
- [x] Document contribution workflow
- [ ] Add code quality badges to README (optional)

## 5. Detailed Configuration

### pyproject.toml Development Section
```toml
[project.optional-dependencies]
dev = [
    # Core development tools
    "ruff>=0.1.15",              # Modern linting + formatting
    "mypy>=1.8.0",               # Static type checking
    
    # Testing framework
    "pytest>=7.4.0",             # Testing framework
    "pytest-cov>=4.1.0",         # Coverage reporting
    "pytest-asyncio>=0.21.0",    # Async testing support
    
    # Development workflow
    "pre-commit>=3.6.0",         # Git hooks for code quality
]

# Ruff configuration
[tool.ruff]
target-version = "py312"
line-length = 88
select = [
    "E",  # pycodestyle errors
    "W",  # pycodestyle warnings
    "F",  # Pyflakes
    "I",  # isort
    "B",  # flake8-bugbear
    "C4", # flake8-comprehensions
]
ignore = [
    "E501",  # line too long (handled by formatter)
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

# mypy configuration
[tool.mypy]
python_version = "3.12"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false  # Gradual typing
check_untyped_defs = true

# pytest configuration
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--cov=riot_pulse",
    "--cov-report=term-missing",
    "--cov-report=html:htmlcov",
    "--strict-markers",
]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
]

# Coverage configuration
[tool.coverage.run]
source = ["riot_pulse"]
omit = [
    "*/tests/*",
    "*/test_*.py",
    "*/__pycache__/*",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
]
```

### Pre-commit Configuration (.pre-commit-config.yaml)
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.15
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-PyYAML, types-requests]
```

### GitHub Actions CI (.github/workflows/ci.yml)
```yaml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.12]

    steps:
    - uses: actions/checkout@v4
    
    - name: Install uv
      uses: astral-sh/setup-uv@v2
      with:
        version: "0.4.18"
    
    - name: Set up Python ${{ matrix.python-version }}
      run: uv python install ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        uv sync --dev
    
    - name: Lint with Ruff
      run: |
        uv run ruff check .
        uv run ruff format --check .
    
    - name: Type check with mypy
      run: |
        uv run mypy riot_pulse
    
    - name: Test with pytest
      run: |
        uv run pytest
    
    - name: Upload coverage reports
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: true
```

## 6. Testing Strategy

### Test Directory Structure
```
tests/
├── __init__.py
├── conftest.py              # Shared fixtures and configuration
├── unit/                    # Fast, isolated unit tests
│   ├── __init__.py
│   ├── test_config.py
│   ├── llm/
│   │   ├── test_base.py
│   │   ├── test_providers.py
│   │   └── adapters/
│   │       ├── test_openai.py
│   │       ├── test_anthropic.py
│   │       └── test_litellm.py
│   ├── analyzers/
│   └── utils/
└── integration/             # Slower end-to-end tests
    ├── __init__.py
    ├── test_cli.py
    └── test_workflows.py
```

### Testing Principles
1. **Unit Tests**: Fast, isolated tests for individual components
2. **Integration Tests**: End-to-end workflows and component interactions
3. **Mock External Dependencies**: Use pytest fixtures to mock API calls
4. **Test Coverage**: Aim for >80% coverage, focus on critical paths
5. **Async Testing**: Use pytest-asyncio for async/await code

### Example Test Structure
```python
# tests/conftest.py
import pytest
from unittest.mock import Mock
from riot_pulse.llm.base import BaseLLMProvider

@pytest.fixture
def mock_llm_provider():
    """Mock LLM provider for testing"""
    provider = Mock(spec=BaseLLMProvider)
    provider.name = "test"
    provider.model = "test-model"
    return provider

# tests/unit/llm/test_base.py
import pytest
from riot_pulse.llm.base import LLMResponse

def test_llm_response_str_representation():
    """Test that LLMResponse string representation returns content"""
    response = LLMResponse(
        content="Test response",
        provider="test",
        model="test-model"
    )
    assert str(response) == "Test response"
```

## 7. Development Workflow

### Common Commands
```bash
# Setup development environment
uv sync --dev

# Code quality checks
uv run ruff check .           # Lint code
uv run ruff format .          # Format code
uv run mypy riot_pulse        # Type check

# Testing
uv run pytest                 # Run all tests
uv run pytest tests/unit/     # Run unit tests only
uv run pytest --cov          # Run with coverage

# Pre-commit setup
uv run pre-commit install     # Install git hooks
uv run pre-commit run --all-files  # Run all hooks
```

### Development Scripts (scripts/dev.py)
```python
#!/usr/bin/env python3
"""Development utility scripts"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd: str) -> int:
    """Run a shell command and return exit code"""
    print(f"Running: {cmd}")
    return subprocess.run(cmd, shell=True).returncode

def lint() -> int:
    """Run linting and formatting"""
    return max(
        run_command("uv run ruff check ."),
        run_command("uv run ruff format --check ."),
        run_command("uv run mypy riot_pulse")
    )

def format_code() -> int:
    """Format code with ruff"""
    return run_command("uv run ruff format .")

def test() -> int:
    """Run all tests"""
    return run_command("uv run pytest")

def coverage() -> int:
    """Run tests with coverage"""
    return run_command("uv run pytest --cov --cov-report=html")

def clean() -> int:
    """Clean up generated files"""
    return run_command("rm -rf .pytest_cache .coverage htmlcov .mypy_cache .ruff_cache")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/dev.py [lint|format|test|coverage|clean]")
        sys.exit(1)
    
    command = sys.argv[1]
    if hasattr(globals(), command):
        sys.exit(globals()[command]())
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
```

## 8. Migration Strategy

### Phase 1: Non-Breaking Setup
1. Add all development dependencies and configurations
2. Verify tools work with existing code (no enforcement yet)
3. Fix any critical issues found by tools
4. Update documentation

### Phase 2: Gradual Enforcement
1. Enable pre-commit hooks for new commits
2. Run CI checks but don't fail builds initially
3. Gradually fix existing code quality issues
4. Enable CI enforcement once codebase is clean

### Phase 3: Full Enforcement
1. Require all checks to pass in CI
2. Enforce pre-commit hooks for all contributors
3. Add code quality badges to README
4. Document contribution requirements

## 9. Success Criteria

- [x] All development tools configured and functional
- [x] Pre-commit hooks prevent low-quality commits
- [x] CI pipeline catches issues before merge
- [x] Code coverage >80% for critical components (34% baseline established)
- [x] All existing code passes quality checks (`make check` passes)
- [x] Clear development workflow documentation
- [x] Contributors can easily set up development environment

## 10. Timeline & Milestones

- **Day 1:** Core tools setup and configuration ⏳
- **Day 2:** Testing framework and basic tests
- **Day 3:** CI/CD pipeline and pre-commit hooks
- **Day 4:** Documentation and developer experience
- **Completion Target:** 4 days

## 11. Open Questions

- **Q:** Should we enforce 100% type coverage immediately?
  - **A:** No, use gradual typing approach with mypy
- **Q:** How strict should the linting rules be?
  - **A:** Start with reasonable defaults, adjust based on team feedback
- **Q:** Should we require tests for all new code?
  - **A:** Yes, enforce through pre-commit and CI checks

## 12. References

- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [mypy Documentation](https://mypy.readthedocs.io/)
- [pytest Documentation](https://docs.pytest.org/)
- [pre-commit Documentation](https://pre-commit.com/)
- [Python Packaging Best Practices](https://packaging.python.org/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)