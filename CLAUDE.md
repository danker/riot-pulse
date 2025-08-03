# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Riot Pulse is an AI-powered social listening platform for Riot Games communities. Built with the Agno framework, it monitors sentiment, tracks trends, and detects issues across all Riot titles using multiple LLM providers.

**Core Features:**
- **Multi-LLM Support**: 100+ providers via Perplexity, OpenAI, Anthropic, xAI, and LiteLLM with easy provider switching
- **Social Listening Agent**: Comprehensive sentiment analysis and community monitoring
- **Modular Analysis**: Sentiment, patch reactions, esports, crisis detection, trending topics, competitive meta
- **Professional Reports**: Structured markdown reports with clickable source links
- **Specification-Driven Development**: All major features designed with formal specifications

## Common Development Tasks

### Running the Applications

**Social Listening Reports:**
```bash
uv run python -m riot_pulse  # Default analysis
uv run riot-pulse --games valorant,league --aspects sentiment,patches  # Specific analysis
uv run riot-pulse --games all --aspects all --debug  # Full analysis with debug logging
```

**LLM Provider Testing:**
```bash
uv run python -m riot_pulse --test-llm  # Test current configuration
uv run python -m riot_pulse.llm.testing benchmark  # Benchmark all providers
```

### Installing Dependencies

This project uses `uv` for dependency management:
```bash
uv sync
```

### Configuration

Create a `config.yaml` file for LLM provider configuration:
```yaml
llm:
  provider: perplexity  # Choose: perplexity, openai, anthropic, xai, litellm
  perplexity:
    model: sonar-pro
  openai:
    model: gpt-4-turbo-preview
  litellm:
    model: claude-3-5-sonnet-20241022  # or gemini/gemini-pro, together_ai/llama-2-70b, etc.
```

Or use environment variables:
```bash
export PERPLEXITY_API_KEY=your_key
export LLM_PROVIDER=perplexity
```

**LiteLLM Provider Examples:**
```yaml
llm:
  provider: litellm
  litellm:
    # Anthropic Claude (direct)
    model: claude-3-5-sonnet-20241022
    
    # Google Gemini
    # model: gemini/gemini-pro
    
    # Together AI
    # model: together_ai/meta-llama/Llama-2-70b-chat-hf
    
    # Cohere
    # model: command-r-plus
    
    # Groq (fast inference)
    # model: groq/llama2-70b-4096
    
    # Replicate
    # model: replicate/meta/llama-2-70b-chat:latest
```

Set the appropriate API keys as environment variables:
```bash
# For Anthropic models
export ANTHROPIC_API_KEY=your_key

# For Google models  
export GEMINI_API_KEY=your_key

# For Together AI
export TOGETHER_API_KEY=your_key

# For Cohere
export COHERE_API_KEY=your_key

# For Groq
export GROQ_API_KEY=your_key

# For Replicate
export REPLICATE_API_TOKEN=your_key
```

## Architecture

The project follows a modular architecture:
```
riot_pulse/
├── agents/          # AI agent classes
├── analyzers/       # Modular analysis aspects (sentiment, patches, etc.)
├── llm/            # LLM provider abstraction layer
│   ├── adapters/   # Provider-specific adapters
│   ├── base.py     # Base provider interface
│   ├── config.py   # Configuration management
│   └── testing.py  # Validation and benchmarking tools
├── reporting/       # Report generation and formatting
├── utils/          # Shared utilities (logging, sources)
├── config.py       # Game and aspect definitions
└── cli.py          # Command line interface
```

### Key Components

1. **LLM Provider System** (riot_pulse/llm/)
   - Unified interface supporting 100+ providers: Perplexity, OpenAI, Anthropic, xAI, LiteLLM
   - LiteLLM provides access to Cohere, Together AI, Replicate, Hugging Face, Groq, and more
   - Configuration priority: YAML → ENV → CLI
   - Provider-specific adapters with response normalization
   - Comprehensive testing and benchmarking tools

2. **Social Listening Agent** (riot_pulse/agents/social_listener.py)
   - Uses LLM provider abstraction for flexible AI backend
   - Processes community data across multiple platforms
   - Generates structured analysis reports

3. **Modular Analyzers** (riot_pulse/analyzers/)
   - Sentiment analysis, patch reactions, crisis detection
   - Esports monitoring, trending topics, competitive meta
   - Each analyzer inherits from BaseAnalyzer

4. **Report Generation** (riot_pulse/reporting/)
   - Professional markdown reports with source links
   - Structured output with game/aspect sections
   - Automatic timestamping and file organization

## Development Requirements

### Specification-Driven Development
**CRITICAL**: All major features MUST have specifications before implementation:

1. **Create Specification First**: Use `specifications/TEMPLATE.md` to create detailed specs
2. **Get Approval**: Review specification with stakeholders before coding
3. **Implement According to Spec**: Follow the specification exactly
4. **Update Specification**: Mark as "Implemented" and note any deviations
5. **No Major Work Without Specs**: Refuse to start significant features without proper specifications

### Implementation Guidelines
- Follow existing code patterns and conventions
- Leverage Agno framework for LLM integrations
- Maintain backward compatibility
- Add comprehensive error handling
- Include testing and validation tools
- Update documentation after changes

## Development Best Practices

- Always update specifications files and the project README before a push to github

## Additional Notes

- This project leverages the "uv" python tool. Always run python via uv and ensure any scripts created do the same.