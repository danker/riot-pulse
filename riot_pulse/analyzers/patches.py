"""
Patch reaction analysis
"""

from .base import BaseAnalyzer
from ..config import RiotGames


class PatchAnalyzer(BaseAnalyzer):
    """Analyzes community reactions to game patches and updates"""
    
    @property
    def name(self) -> str:
        return "Patch Reaction Analysis"
    
    @property
    def description(self) -> str:
        return "Monitors community reactions to game patches, balance changes, and updates"
    
    def generate_query(self, game: RiotGames, timeframe: str = "24 hours") -> str:
        game_name = RiotGames.get_display_name(game)
        
        return f"""Analyze community reactions to recent {game_name} patches and updates in the past {timeframe}.
        
Focus on:
- Latest patch notes and balance changes
- Community reception of changes
- Balance complaints or praise
- Meta shift discussions
- Pro player and content creator reactions
- Bug reports and technical issues

Areas to examine:
- Character/agent/champion balance changes
- Item/weapon adjustments
- Map changes or updates
- New features or content
- Quality of life improvements
- Performance optimizations

Sources to check:
- Official patch notes and dev blogs
- Reddit patch discussion threads
- Twitter reactions from pros and influencers
- Gaming forums and community sites
- Twitch/YouTube content about patches

Provide:
1. Summary of recent patches/updates
2. Overall community reception
3. Most controversial changes
4. Positive feedback highlights
5. Emerging meta discussions
6. Technical issues reported

Include specific patch versions, dates, and source URLs."""