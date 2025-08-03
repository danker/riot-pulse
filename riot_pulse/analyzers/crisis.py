"""
Crisis detection and monitoring
"""

from .base import BaseAnalyzer
from ..config import RiotGames


class CrisisAnalyzer(BaseAnalyzer):
    """Detects potential PR crises and negative sentiment spikes"""
    
    @property
    def name(self) -> str:
        return "Crisis Detection"
    
    @property
    def description(self) -> str:
        return "Monitors for potential PR issues, controversies, and negative sentiment spikes"
    
    def generate_query(self, game: RiotGames, timeframe: str = "24 hours") -> str:
        game_name = RiotGames.get_display_name(game)
        
        return f"""Monitor for potential crises, controversies, or significant negative sentiment around {game_name} in the past {timeframe}.
        
Look for:
- Major community backlash or outrage
- Controversial decisions or announcements
- Technical issues causing widespread problems
- Security breaches or data concerns
- Inappropriate behavior by players/staff
- Boycotts or protest movements
- Viral negative content or memes

Crisis indicators to detect:
- Sudden spikes in negative mentions
- Trending negative hashtags
- High-engagement complaint threads
- News coverage of issues
- Influencer/streamer criticisms
- Official apologies or responses

Sources to monitor:
- Reddit drama and complaint threads
- Twitter/X trending topics and mentions
- Gaming news sites covering controversies
- Official Riot responses or statements
- Streamer reactions and community discussions
- Gaming forums and Discord communities

Assessment framework:
1. Severity Level (Low/Medium/High/Critical)
2. Scope (Local community/Regional/Global)
3. Root cause analysis
4. Community sentiment trajectory
5. Official response status
6. Potential impact assessment

For each issue found:
- Describe the controversy or problem
- Assess severity and potential impact
- Track community sentiment and engagement
- Note any official responses
- Provide recommendation for monitoring

If no significant issues detected, state "No major crises detected" and provide brief summary of minor concerns if any.

Include specific sources, timestamps, and engagement metrics where available."""