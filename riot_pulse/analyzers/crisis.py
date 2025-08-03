"""
Crisis detection and monitoring
"""

from .base import BaseAnalyzer
from ..config import RiotGames
from ..utils.query_enhancer import QueryEnhancer


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
        
        base_query = f"""URGENT: Crisis monitoring scan for {game_name} - detect ANY emerging issues, controversies, or negative sentiment spikes.

CRITICAL CRISIS INDICATORS:
- Community backlash, outrage, or coordinated negative campaigns
- Technical disasters (server outages, game-breaking bugs, security breaches)
- Controversial announcements, policy changes, or developer decisions
- Professional player or content creator scandals/criticisms
- Boycott movements, review bombing, or organized protests
- Viral negative content, memes, or social media trends
- Official emergency responses, apologies, or damage control statements

THREAT ASSESSMENT FRAMEWORK:
1. SEVERITY LEVEL:
   - CRITICAL: Trending globally, major media coverage, potential legal/regulatory issues
   - HIGH: Widespread community anger, significant engagement drops, streamer boycotts
   - MEDIUM: Localized complaints, moderate negative sentiment, manageable scope
   - LOW: Minor grumbling, isolated incidents, normal community friction

2. IMPACT ANALYSIS:
   - Player base reaction and potential churn risk
   - Media coverage and PR damage assessment
   - Financial implications (stock impact, revenue threats)
   - Timeline and escalation potential
   - Official response adequacy and effectiveness

EMERGENCY RESPONSE INDICATORS:
- Official Riot statements, blog posts, or emergency patches
- Emergency developer streams or community communications
- Sudden changes to game features, policies, or events
- Legal notices, compliance updates, or regulatory responses

OUTPUT REQUIREMENTS:
- If NO crisis detected: State "NO MAJOR CRISES DETECTED" and summarize minor concerns
- If crisis found: Provide immediate threat assessment with specific evidence
- Include real-time social media metrics (upvotes, retweets, engagement)
- Link to primary source discussions and official responses
- Assess whether situation is escalating, stable, or de-escalating"""

        return QueryEnhancer.enhance_query(base_query, game, timeframe)