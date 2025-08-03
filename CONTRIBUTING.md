# Contributing to Riot Pulse

Thank you for your interest in contributing to Riot Pulse! This document provides guidelines and information for contributors.

## Development Setup

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) for package management
- Git

### Setting Up Your Development Environment

1. **Fork and Clone**
   ```bash
   git clone https://github.com/yourusername/riot-pulse.git
   cd riot-pulse
   ```

2. **Install Dependencies**
   ```bash
   uv sync --dev
   ```

3. **Set Up Pre-commit Hooks**
   ```bash
   uv run pre-commit install
   ```

4. **Verify Setup**
   ```bash
   make check
   # or
   python scripts/dev.py check
   ```

## Development Workflow

### Making Changes

1. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Follow the coding standards below
   - Write tests for new functionality
   - Update documentation as needed

3. **Run Quality Checks**
   ```bash
   make check  # Runs linting + tests
   ```

4. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

5. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

### Commit Message Convention

We use conventional commits for clear changelog generation:

- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

Example: `feat: add LiteLLM provider support for 100+ models`

## Coding Standards

### Code Quality Tools

We use modern Python tooling for consistent code quality:

- **Ruff**: Fast linting and formatting (replaces black, isort, flake8)
- **mypy**: Static type checking
- **pytest**: Testing framework with coverage reporting
- **pre-commit**: Automated quality checks

### Code Style

- **Line Length**: 88 characters (managed by ruff)
- **Quotes**: Double quotes for strings
- **Imports**: Sorted automatically by ruff
- **Type Hints**: Required for all public functions and classes

### Type Checking

- Use type hints for all function parameters and return values
- Import types from `typing` module when needed
- Use `Optional[T]` for nullable values
- All code must pass `mypy` checks

Example:
```python
from typing import Dict, Any, Optional

def process_config(config: Dict[str, Any]) -> Optional[str]:
    """Process configuration and return result."""
    if not config:
        return None
    return str(config.get("value", "default"))
```

## Testing Guidelines

### Test Structure

```
tests/
├── unit/           # Fast, isolated unit tests
├── integration/    # End-to-end integration tests
└── conftest.py     # Shared fixtures
```

### Writing Tests

- **Unit Tests**: Test individual functions/classes in isolation
- **Integration Tests**: Test component interactions and workflows
- **Use Fixtures**: Leverage pytest fixtures for common test data
- **Mock External Dependencies**: Use `unittest.mock` for API calls

Example test:
```python
import pytest
from unittest.mock import Mock

def test_llm_response_creation(sample_llm_response):
    """Test LLM response object creation."""
    assert sample_llm_response.content == "Test response"
    assert sample_llm_response.provider == "test-provider"
```

### Running Tests

```bash
# All tests
make test

# Unit tests only
make test-unit

# Integration tests only  
make test-int

# With coverage
make coverage
```

## Documentation

### Code Documentation

- **Docstrings**: Use Google-style docstrings for all public functions
- **Type Hints**: Comprehensive type annotations
- **Comments**: Explain complex logic, not obvious code

Example:
```python
def analyze_sentiment(text: str, provider: str = "openai") -> Dict[str, Any]:
    """
    Analyze sentiment of the given text using specified LLM provider.
    
    Args:
        text: The text to analyze for sentiment
        provider: LLM provider to use (default: "openai")
        
    Returns:
        Dictionary containing sentiment analysis results with keys:
        - sentiment: Overall sentiment (positive/negative/neutral)
        - confidence: Confidence score (0.0-1.0)
        - details: Detailed analysis breakdown
        
    Raises:
        ValueError: If text is empty or provider is unsupported
    """
```

### README and Specifications

- Update README.md for user-facing changes
- Create specifications for major features (see `specifications/TEMPLATE.md`)
- Keep documentation up-to-date with code changes

## Development Commands

We provide several commands to streamline development:

### Make Commands
```bash
make help           # Show all available commands
make dev-setup      # Complete development setup
make lint           # Run linting and type checking
make format         # Format code with ruff
make test           # Run all tests
make coverage       # Run tests with coverage
make check          # Run all quality checks
make clean          # Clean generated files
```

### Python Script Commands
```bash
python scripts/dev.py help       # Show detailed help
python scripts/dev.py lint       # Lint code
python scripts/dev.py format     # Format code
python scripts/dev.py test       # Run tests
python scripts/dev.py coverage   # Generate coverage
python scripts/dev.py check      # All quality checks
python scripts/dev.py clean      # Clean up files
```

## Architecture Guidelines

### Adding New LLM Providers

1. Create adapter in `riot_pulse/llm/adapters/`
2. Inherit from `BaseLLMProvider`
3. Implement required methods
4. Register with `LLMProviderRegistry`
5. Add tests in `tests/unit/llm/adapters/`

### Adding New Analysis Aspects

1. Create analyzer in `riot_pulse/analyzers/`
2. Inherit from `BaseAnalyzer`
3. Add to `AnalysisAspects` enum
4. Register in `analyzers/__init__.py`
5. Add tests and documentation

### Specification-Driven Development

For major features:
1. Create specification using `specifications/TEMPLATE.md`
2. Get review and approval on specification
3. Implement according to specification
4. Update specification with implementation notes

## Pull Request Guidelines

### Before Submitting

- [ ] All tests pass (`make test`)
- [ ] Code passes linting (`make lint`)  
- [ ] Type checking passes (`make mypy`)
- [ ] Coverage remains above 80%
- [ ] Documentation is updated
- [ ] Pre-commit hooks are satisfied

### PR Description Template

```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring
- [ ] Other (please describe)

## Testing
- [ ] Added/updated unit tests
- [ ] Added/updated integration tests
- [ ] Manual testing performed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated and passing
```

## Getting Help

- **Issues**: Check existing [GitHub issues](https://github.com/danker/riot-pulse/issues)
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: See README.md and specifications/

## Recognition

Contributors are recognized in:
- Git commit history
- Release notes for significant contributions
- README acknowledgments for major features

Thank you for contributing to Riot Pulse! 🎮