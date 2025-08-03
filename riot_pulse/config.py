"""
Configuration and constants for Riot Pulse
"""

from dataclasses import dataclass
from enum import Enum


class RiotGames(Enum):
    """Enumeration of Riot Games titles"""

    VALORANT = "valorant"
    LEAGUE_OF_LEGENDS = "league_of_legends"
    TEAMFIGHT_TACTICS = "teamfight_tactics"
    LEGENDS_OF_RUNETERRA = "legends_of_runeterra"
    TWOXKO = "2xko"
    RIFTBOUND = "riftbound"

    @classmethod
    def get_display_name(cls, game: "RiotGames") -> str:
        """Get human-readable display name for a game"""
        display_names = {
            cls.VALORANT: "VALORANT",
            cls.LEAGUE_OF_LEGENDS: "League of Legends",
            cls.TEAMFIGHT_TACTICS: "Teamfight Tactics",
            cls.LEGENDS_OF_RUNETERRA: "Legends of Runeterra",
            cls.TWOXKO: "2XKO",
            cls.RIFTBOUND: "Riftbound",
        }
        return display_names.get(game, game.value)

    @classmethod
    def from_string(cls, game_str: str) -> "RiotGames":
        """Create RiotGames enum from string (case insensitive)"""
        game_str = game_str.lower().replace(" ", "_").replace("-", "_")

        # Handle common aliases
        aliases = {
            "lol": cls.LEAGUE_OF_LEGENDS,
            "league": cls.LEAGUE_OF_LEGENDS,
            "val": cls.VALORANT,
            "tft": cls.TEAMFIGHT_TACTICS,
            "lor": cls.LEGENDS_OF_RUNETERRA,
            "runeterra": cls.LEGENDS_OF_RUNETERRA,
            "2xko": cls.TWOXKO,
            "riftbound": cls.RIFTBOUND,
        }

        if game_str in aliases:
            return aliases[game_str]

        # Try exact match
        for game in cls:
            if game.value == game_str:
                return game

        raise ValueError(f"Unknown game: {game_str}")


class AnalysisAspects(Enum):
    """Types of analysis that can be performed"""

    SENTIMENT = "sentiment"
    PATCHES = "patches"
    ESPORTS = "esports"
    CRISIS = "crisis"
    TRENDING = "trending"
    META = "meta"

    @classmethod
    def get_display_name(cls, aspect: "AnalysisAspects") -> str:
        """Get human-readable display name for an analysis aspect"""
        display_names = {
            cls.SENTIMENT: "Community Sentiment",
            cls.PATCHES: "Patch Analysis",
            cls.ESPORTS: "Esports Scene",
            cls.CRISIS: "Crisis Detection",
            cls.TRENDING: "Trending Topics",
            cls.META: "Competitive Meta",
        }
        return display_names.get(aspect, aspect.value)


@dataclass
class ReportConfig:
    """Configuration for a report generation run"""

    games: list[RiotGames]
    aspects: list[AnalysisAspects]
    timeframe: str = "24 hours"
    debug_mode: bool = False
    output_format: str = "markdown"

    @classmethod
    def from_cli_args(
        cls, games: list[str], aspects: list[str], **kwargs
    ) -> "ReportConfig":
        """Create ReportConfig from CLI arguments"""
        # Handle "all" keyword for games
        if "all" in games:
            riot_games = list(RiotGames)
        else:
            riot_games = [RiotGames.from_string(g) for g in games]

        # Handle "all" keyword for aspects
        if "all" in aspects:
            analysis_aspects = list(AnalysisAspects)
        else:
            analysis_aspects = [AnalysisAspects(a.lower()) for a in aspects]

        return cls(games=riot_games, aspects=analysis_aspects, **kwargs)


# Default configurations
DEFAULT_GAMES = [RiotGames.VALORANT, RiotGames.LEAGUE_OF_LEGENDS]
DEFAULT_ASPECTS = [
    AnalysisAspects.SENTIMENT,
    AnalysisAspects.PATCHES,
    AnalysisAspects.CRISIS,
]

PERPLEXITY_CONFIG = {
    "model_id": "sonar-pro",
    "instructions": [
        "You are a gaming industry analyst specializing in Riot Games",
        "Focus on community sentiment, competitive meta, and player feedback",
        "Always provide specific sources and actionable insights",
        "Structure responses with clear sections: Summary, Key Themes, Sentiment, Sources",
    ],
}
