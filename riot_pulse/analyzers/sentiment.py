"""
Community sentiment analysis
"""

from ..config import RiotGames
from ..utils.query_enhancer import QueryEnhancer
from .base import BaseAnalyzer


class SentimentAnalyzer(BaseAnalyzer):
    """Analyzes community sentiment for a specific game"""

    @property
    def name(self) -> str:
        return "Community Sentiment Analysis"

    @property
    def description(self) -> str:
        return "Analyzes player sentiment across social media, forums, and gaming communities"

    def generate_query(self, game: RiotGames, timeframe: str = "24 hours") -> str:
        game_name = RiotGames.get_display_name(game)

        base_query = f"""Analyze community sentiment for {game_name} in the gaming community.

ANALYSIS FOCUS:
- Overall community mood and player satisfaction levels
- Common praise, complaints, and feedback themes
- Player engagement and retention discussions
- Community reaction to recent updates or events
- Sentiment trends and shifts in perception

REQUIRED OUTPUT FORMAT:
1. Sentiment Score: [Very Positive/Positive/Neutral/Negative/Very Negative]
2. Key Sentiment Drivers: [Top 3-5 themes with specific examples]
3. Community Highlights: [Notable positive discussions or achievements]
4. Pain Points: [Major complaints or concerns with context]
5. Trending Conversations: [Current hot topics in the community]

EVIDENCE REQUIREMENTS:
- Include direct quotes from community posts when possible
- Provide specific post titles, usernames, and engagement metrics
- Reference multiple sources to support each sentiment claim
- Note any conflicting viewpoints or debates within the community"""

        return QueryEnhancer.enhance_query(base_query, game, timeframe)
