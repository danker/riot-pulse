# Riot Pulse 🎮

AI-powered social listening platform for Riot Games communities. Monitor sentiment, track trends, and detect issues across all Riot titles using advanced AI analysis.

## Features

- **🎯 Multi-Game Support**: VALORANT, League of Legends, Teamfight Tactics, Legends of Runeterra, 2XKO, Riftbound, and more
- **📊 Comprehensive Analysis**: Sentiment, patch reactions, esports scene, crisis detection, trending topics, and competitive meta
- **🤖 AI-Powered**: Uses Perplexity AI for real-time social media and community analysis
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

Create a `.env` file with your Perplexity API key:

```bash
PERPLEXITY_API_KEY=your_api_key_here
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
```

## Architecture

```
riot_pulse/
├── agents/          # AI agent classes
├── analyzers/       # Modular analysis aspects
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

### Running Tests

```bash
# Install development dependencies
uv sync --dev

# Run the application
uv run riot-pulse --games valorant --aspects sentiment
```

## Requirements

- Python 3.12+
- Perplexity AI API key
- Internet connection for real-time analysis

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Built with [Agno AI framework](https://github.com/agno-ai/agno)
- Powered by [Perplexity AI](https://perplexity.ai)
- Community data from Reddit, Twitter, gaming forums, and official sources