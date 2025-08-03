"""
Esports scene analysis
"""

from .base import BaseAnalyzer
from ..config import RiotGames


class EsportsAnalyzer(BaseAnalyzer):
    """Analyzes esports scene activity and community engagement"""
    
    @property
    def name(self) -> str:
        return "Esports Scene Analysis"
    
    @property
    def description(self) -> str:
        return "Monitors competitive scene, tournaments, and professional player activity"
    
    def generate_query(self, game: RiotGames, timeframe: str = "24 hours") -> str:
        game_name = RiotGames.get_display_name(game)
        
        # Customize query based on game
        tournament_info = self._get_tournament_context(game)
        
        return f"""Analyze the {game_name} esports scene activity over the past {timeframe}.
        
Focus on:
- Recent tournament results and highlights
- Professional player news and transfers
- Team announcements and roster changes
- Community reactions to competitive matches
- Viewership and engagement metrics
- Upcoming tournament announcements

{tournament_info}

Areas to examine:
- Major tournament results and standout performances
- Player transfers, signings, and roster moves
- Community reactions to competitive matches
- Viewership numbers and engagement
- Coaching changes and organizational news
- Rule changes or format updates

Sources to check:
- Official esports news and announcements
- Team and player social media
- Esports news sites (ESPN Esports, Dot Esports, etc.)
- Reddit esports communities
- Twitch/YouTube tournament content
- Professional player streams and content

Provide:
1. Recent tournament/match highlights
2. Major player or team news
3. Community engagement with competitive scene
4. Notable performances or upsets
5. Upcoming events to watch
6. Viewership trends if available

Include specific match results, dates, and source URLs."""
    
    def _get_tournament_context(self, game: RiotGames) -> str:
        """Get game-specific tournament context"""
        contexts = {
            RiotGames.VALORANT: """
Tournament context:
- VCT (VALORANT Champions Tour) - Premier global competition
- Regional leagues (Americas, EMEA, Pacific)
- Masters and Champions events
- Game Changers series""",
            
            RiotGames.LEAGUE_OF_LEGENDS: """
Tournament context:
- LCS, LEC, LCK, LPL - Major regional leagues
- MSI (Mid-Season Invitational) and Worlds Championship
- Regional tournaments and qualifying events
- Academy and development leagues""",
            
            RiotGames.TEAMFIGHT_TACTICS: """
Tournament context:
- TFT World Championship and regional championships
- Set releases and competitive meta changes
- Challenger tournaments and qualifier events
- Content creator tournaments""",
        }
        
        return contexts.get(game, "Check for any organized competitive events or tournaments.")