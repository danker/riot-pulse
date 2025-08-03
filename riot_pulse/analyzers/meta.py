"""
Competitive meta analysis
"""

from ..config import RiotGames
from .base import BaseAnalyzer


class MetaAnalyzer(BaseAnalyzer):
    """Analyzes competitive meta and strategic trends"""

    @property
    def name(self) -> str:
        return "Competitive Meta Analysis"

    @property
    def description(self) -> str:
        return "Tracks competitive meta shifts, tier lists, and strategic trends"

    def generate_query(self, game: RiotGames, timeframe: str = "24 hours") -> str:
        game_name = RiotGames.get_display_name(game)

        # Customize query based on game specifics
        meta_context = self._get_meta_context(game)

        return f"""Analyze the current competitive meta and strategic trends for {game_name} over the past {timeframe}.

{meta_context}

Focus areas:
- Current tier lists and character/agent rankings
- Popular strategies and compositions
- Pro player picks and preferences
- Community meta discussions and debates
- Emerging strategies or innovations
- Counter-strategies and adaptations

Sources to analyze:
- Professional match data and statistics
- Tier list websites and community rankings
- Pro player streams and commentary
- Strategy guides and analysis content
- Reddit meta discussions
- Coach and analyst insights

Meta shift indicators:
- Changes in pick/ban rates
- New strategy discoveries
- Professional tournament adaptations
- Patch impact on meta evolution
- Community adoption of pro strategies
- Counter-meta developments

Provide analysis on:
1. Current meta overview and dominant strategies
2. Recent shifts or emerging trends
3. Community vs. professional meta differences
4. Controversial picks or strategies
5. Future meta predictions based on trends
6. Impact of recent changes on competitive play

Include specific statistics, pro player examples, and source URLs where available."""

    def _get_meta_context(self, game: RiotGames) -> str:
        """Get game-specific meta analysis context"""
        contexts = {
            RiotGames.VALORANT: """
Meta elements to track:
- Agent pick rates and compositions
- Map-specific strategies and setups
- Weapon preferences and economy strategies
- Team coordination tactics and executes
- Anti-stratting and counter-play developments""",
            RiotGames.LEAGUE_OF_LEGENDS: """
Meta elements to track:
- Champion pick/ban rates by role
- Jungle pathing and objective priorities
- Lane assignments and flex picks
- Itemization trends and build paths
- Team fighting strategies and win conditions""",
            RiotGames.TEAMFIGHT_TACTICS: """
Meta elements to track:
- Dominant team compositions and synergies
- Optimal itemization strategies
- Positioning and board management
- Economic strategies and tempo plays
- Flexible vs. forcing strategies""",
        }

        return contexts.get(game, "Analyze strategic trends and competitive patterns.")
