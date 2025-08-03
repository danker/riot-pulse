"""
Trending topics analysis
"""

from .base import BaseAnalyzer
from ..config import RiotGames


class TrendingAnalyzer(BaseAnalyzer):
    """Identifies trending topics and viral content"""
    
    @property
    def name(self) -> str:
        return "Trending Topics"
    
    @property
    def description(self) -> str:
        return "Identifies viral content, trending discussions, and emerging topics"
    
    def generate_query(self, game: RiotGames, timeframe: str = "24 hours") -> str:
        game_name = RiotGames.get_display_name(game)
        
        return f"""Identify trending topics and viral content related to {game_name} in the past {timeframe}.
        
Look for:
- Viral clips, plays, or moments
- Trending memes and community jokes
- Popular fan art, cosplay, or creative content
- Breaking news or announcements
- Influencer collaborations or events
- Community challenges or movements
- Surprising or unexpected moments

Content types to track:
- High-engagement social media posts
- Viral TikTok or YouTube videos
- Popular Reddit threads and discussions
- Trending hashtags and topics
- Streamer highlights and reactions
- Community-created content and art
- News articles gaining traction

Engagement metrics to consider:
- View counts and shares
- Comments and engagement rates
- Cross-platform spread
- Influencer amplification
- Community participation levels

Sources to check:
- Reddit hot and trending posts
- Twitter/X trending topics and viral tweets
- TikTok trending videos
- YouTube trending gaming content
- Twitch clips and highlights
- Gaming news site popular articles
- Discord community discussions

For each trending topic:
1. Topic description and context
2. Engagement level and reach
3. Key platforms where it's trending
4. Notable participants or creators
5. Community sentiment around the topic
6. Potential longevity or staying power

Rank topics by:
- Overall engagement and reach
- Cross-platform penetration
- Community participation
- Novelty and uniqueness
- Potential impact on game community

Include specific URLs, engagement numbers, and timestamps where available."""