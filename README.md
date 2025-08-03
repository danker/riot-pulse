# Riot Pulse 🎮

AI-powered social listening platform for Riot Games communities. Monitor sentiment, track trends, and detect issues across all Riot titles using advanced AI analysis.

## Features

- **🎯 Multi-Game Support**: VALORANT, League of Legends, Teamfight Tactics, Legends of Runeterra, 2XKO, Riftbound, and more
- **📊 Comprehensive Analysis**: Sentiment, patch reactions, esports scene, crisis detection, trending topics, and competitive meta
- **🤖 Multi-LLM Support**: Choose from 100+ providers via Perplexity, OpenAI, Anthropic, xAI, or LiteLLM for analysis
- **⚡ Modular Architecture**: Easy to extend with new games and analysis types
- **📝 Professional Reports**: Generates detailed markdown reports with sources
- **🔧 Flexible CLI**: Configurable games, aspects, and timeframes

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/danker/riot-pulse.git
cd riot-pulse

# Install dependencies with uv
uv sync
```

### Environment Setup

Create a `.env` file with your API keys (choose your preferred LLM provider):

```bash
# At least one API key is required
PERPLEXITY_API_KEY=your_perplexity_key_here
OPENAI_API_KEY=your_openai_key_here  
ANTHROPIC_API_KEY=your_anthropic_key_here
XAI_API_KEY=your_xai_key_here

# For LiteLLM (enables 100+ additional providers)
COHERE_API_KEY=your_cohere_key_here
TOGETHER_API_KEY=your_together_key_here
GROQ_API_KEY=your_groq_key_here
REPLICATE_API_TOKEN=your_replicate_token_here
GEMINI_API_KEY=your_gemini_key_here
```

Or create a `config.yaml` file for more advanced configuration:

```yaml
llm:
  provider: perplexity  # Choose: perplexity, openai, anthropic, xai, litellm
  perplexity:
    model: sonar-pro
  openai:
    model: gpt-4-turbo-preview
  anthropic:
    model: claude-3-opus-20240229
  xai:
    model: grok-1
  litellm:
    model: claude-3-5-sonnet-20241022  # Access to 100+ models
    # Examples: gemini/gemini-pro, together_ai/llama-2-70b, groq/mixtral-8x7b
```

### Basic Usage

```bash
# Default analysis (VALORANT + League, sentiment + patches + crisis)
uv run python -m riot_pulse

# Analyze specific games and aspects
uv run riot-pulse --games valorant,league --aspects sentiment,patches

# Full analysis across all games
uv run riot-pulse --games all --aspects all

# Crisis monitoring with debug logging
uv run riot-pulse --games all --aspects crisis --debug
```

## Available Options

### Games
- `valorant` (alias: `val`) - VALORANT
- `league_of_legends` (alias: `lol`, `league`) - League of Legends  
- `teamfight_tactics` (alias: `tft`) - Teamfight Tactics
- `legends_of_runeterra` (alias: `lor`, `runeterra`) - Legends of Runeterra
- `2xko` - 2XKO (Fighting Game)
- `riftbound` - Riftbound (Physical Card Game)
- `all` - All available games

### Analysis Aspects
- `sentiment` - Community sentiment analysis
- `patches` - Patch reaction monitoring  
- `esports` - Competitive scene activity
- `crisis` - Crisis detection and monitoring
- `trending` - Viral content and trending topics
- `meta` - Competitive meta analysis
- `all` - All analysis aspects

### CLI Examples

```bash
# List available options
uv run riot-pulse --list-games
uv run riot-pulse --list-aspects

# Analyze VALORANT sentiment over past week
uv run riot-pulse --games valorant --aspects sentiment --timeframe "1 week"

# Monitor all games for potential issues
uv run riot-pulse --games all --aspects crisis

# Full competitive analysis
uv run riot-pulse --games valorant,league --aspects esports,meta

# Debug mode with detailed logging
uv run riot-pulse --games valorant --aspects all --debug

# Switch LLM providers
uv run riot-pulse --llm-provider openai --games valorant --aspects sentiment
uv run riot-pulse --llm-provider anthropic --llm-model claude-3-sonnet-20240229
uv run riot-pulse --llm-provider litellm --games valorant --aspects sentiment
```

### LLM Provider Management

```bash
# Test your LLM configuration
uv run python -m riot_pulse --test-llm

# Test specific provider setup
uv run python -m riot_pulse --test-llm --llm-provider openai

# List available providers and models
uv run python -m riot_pulse.llm.testing list

# Benchmark provider performance (requires API keys)
uv run python -m riot_pulse.llm.testing benchmark
```

## Architecture

```
riot_pulse/
├── agents/          # AI agent classes
├── analyzers/       # Modular analysis aspects
├── llm/            # LLM provider abstraction layer
│   ├── adapters/   # Provider-specific adapters
│   ├── base.py     # Base provider interface
│   ├── config.py   # LLM configuration management
│   └── testing.py  # Testing and validation tools
├── reporting/       # Report generation and formatting
├── utils/          # Shared utilities (logging, sources)
├── config.py       # Game and aspect definitions
└── cli.py          # Command line interface
```

## Report Output

Reports are generated in `reports/` directory with format:
- **Filename**: `riot-pulse-report-MM.DD.YYYY.N.md`
- **Content**: Structured markdown with sections for each game/aspect
- **Sources**: Clickable URLs for all claims and data points
- **Logs**: Detailed execution logs in `logs/` directory

## Development

### Adding New Games

1. Add game to `RiotGames` enum in `config.py`
2. Update display names and aliases
3. Customize analysis queries in relevant analyzers

### Adding New Analysis Aspects

1. Create new analyzer in `analyzers/` directory
2. Inherit from `BaseAnalyzer`
3. Register in `analyzers/__init__.py`
4. Add to `AnalysisAspects` enum

### Adding New LLM Providers

1. Create adapter in `llm/adapters/` directory
2. Inherit from `BaseLLMProvider`
3. Implement required methods (`query`, `validate_config`, etc.)
4. Register with `LLMProviderRegistry.register()`

### Development Setup

```bash
# Install development dependencies
uv sync --dev

# Set up development environment (includes pre-commit hooks)
make dev-setup
# or
python scripts/dev.py install && python scripts/dev.py pre-commit
```

### Code Quality and Testing

```bash
# Run linting and type checking
make lint
# or
python scripts/dev.py lint

# Format code
make format
# or  
python scripts/dev.py format

# Run all tests
make test
# or
python scripts/dev.py test

# Run tests with coverage
make coverage
# or
python scripts/dev.py coverage

# Run all quality checks (lint + test)
make check
# or
python scripts/dev.py check
```

### LLM Provider Testing

```bash
# Test LLM configuration
uv run python -m riot_pulse --test-llm

# Test specific provider
uv run python -m riot_pulse.llm.testing dry-run --provider openai

# Benchmark all providers (requires API keys)
uv run python -m riot_pulse.llm.testing benchmark
```

## Requirements

- Python 3.12+
- At least one LLM provider API key:
  - **Perplexity AI** (recommended for web search capabilities)
  - **OpenAI** (GPT-4, GPT-4 Turbo, GPT-3.5)
  - **Anthropic** (Claude 3 Opus, Sonnet, Haiku)
  - **xAI** (Grok-1, Grok-Beta)
  - **LiteLLM** (100+ providers: Cohere, Together AI, Replicate, Hugging Face, Groq, Gemini, and more)
- Internet connection for real-time analysis

## Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository** and create a feature branch
2. **Set up development environment**: `make dev-setup`
3. **Make your changes** following our coding standards
4. **Write tests** for new functionality
5. **Run quality checks**: `make check` (linting + tests must pass)
6. **Submit a pull request** with a clear description

### Development Standards

- **Code Quality**: All code must pass `ruff` linting and formatting
- **Type Checking**: Use type hints, code must pass `mypy` checks  
- **Testing**: Write tests for new features, maintain >80% coverage
- **Pre-commit Hooks**: Automatically enforce code quality standards
- **Specification-Driven**: Major features require specifications (see `specifications/`)

### Quick Development Commands

```bash
make help           # Show all available commands
make dev-setup      # Set up development environment
make check          # Run all quality checks
make test           # Run tests
make coverage       # Generate coverage report
```

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Built with [Agno AI framework](https://github.com/agno-ai/agno)
- LLM Support: [Perplexity AI](https://perplexity.ai), [OpenAI](https://openai.com), [Anthropic](https://anthropic.com), [xAI](https://x.ai), [LiteLLM](https://litellm.ai)
- 100+ Additional Providers via LiteLLM: Cohere, Together AI, Replicate, Hugging Face, Groq, Gemini, and more
- Community data from Reddit, Twitter, gaming forums, and official sources