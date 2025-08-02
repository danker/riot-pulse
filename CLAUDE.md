# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Riot Pulse is an AI-powered social listening platform for Riot Games communities. Built with the Agno framework, it monitors sentiment, tracks trends, and detects issues across all Riot titles. The project includes:

**Core Social Listening Agent** (`riot_social_listener.py`):
- Sentiment analysis across Reddit, Twitter, and gaming forums
- Patch reaction monitoring for community response tracking
- Crisis detection for early warning on controversies
- Trending topic identification across all Riot games

**Interactive Playground** (`playground.py`):
- Web Agent: Uses DuckDuckGo search tools for web searches
- Finance Agent: Uses YFinance tools for financial data analysis

## Common Development Tasks

### Running the Applications

**Social Listening Reports:**
```bash
python riot_social_listener.py
python riot_social_listener.py --debug  # With detailed logging
```

**Interactive Playground:**
```bash
python playground.py
```

This starts a FastAPI server with the Agno playground interface where you can interact with both agents.

### Installing Dependencies

This project uses `uv` for dependency management:
```bash
uv sync
```

### Running Individual Scripts

For basic testing:
```bash
python main.py
```

## Architecture

The project follows a simple structure:
- `playground.py`: Main application file that sets up the Agno playground with two agents
- Agent storage: SQLite database stored in `tmp/agents.db` for persisting agent conversations
- Dependencies: Managed through `pyproject.toml` using modern Python packaging

### Key Components

1. **Web Agent** (playground.py:10-25)
   - GPT-4o based agent with DuckDuckGo search capabilities
   - Configured to always include sources in responses
   - Maintains conversation history (last 5 responses)

2. **Finance Agent** (playground.py:27-37)
   - GPT-4o based agent with YFinance tools
   - Provides stock prices, analyst recommendations, company info, and news
   - Configured to display data in tables

3. **Storage**: Both agents use SQLite storage for session persistence, stored in `tmp/agents.db`

## Development Notes

- The playground runs with auto-reload enabled for development
- Agents are configured with markdown formatting for better readability
- Each agent has its own table in the SQLite database for session isolation