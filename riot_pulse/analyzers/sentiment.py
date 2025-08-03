"""
Community sentiment analysis
"""

from .base import BaseAnalyzer
from ..config import RiotGames


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
        
        return f"""Analyze community sentiment for {game_name} over the past {timeframe}.
        
Focus on:
- Overall community mood and satisfaction
- Common praise and complaints
- Player engagement levels
- Social media mentions and discussions
- Reddit/Discord sentiment trends
- Streamer and content creator opinions

Sources to check:
- Reddit (r/{game_name.lower().replace(' ', '')}, r/riotgames)
- Twitter/X mentions and hashtags
- Gaming forums and communities
- Twitch/YouTube content and comments
- Discord communities

Provide:
1. Overall sentiment score (Very Positive/Positive/Neutral/Negative/Very Negative)
2. Key themes driving sentiment
3. Specific examples with sources
4. Trending topics or discussions
5. Notable changes from previous periods

Include specific URLs and sources for all claims."""