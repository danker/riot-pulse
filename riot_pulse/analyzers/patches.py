"""
Patch reaction analysis
"""

from ..config import RiotGames
from ..utils.query_enhancer import QueryEnhancer
from .base import BaseAnalyzer


class PatchAnalyzer(BaseAnalyzer):
    """Analyzes community reactions to game patches and updates"""

    @property
    def name(self) -> str:
        return "Patch Reaction Analysis"

    @property
    def description(self) -> str:
        return (
            "Monitors community reactions to game patches, balance changes, and updates"
        )

    def generate_query(self, game: RiotGames, timeframe: str = "24 hours") -> str:
        game_name = RiotGames.get_display_name(game)

        base_query = f"""Analyze recent {game_name} patch reactions and community response to game updates.

PATCH TRACKING PRIORITIES:
- Identify the most recent patch version number and release date
- Track immediate community response to balance changes
- Monitor professional player and content creator first impressions
- Detect emerging gameplay meta shifts and strategies
- Identify any game-breaking bugs or technical issues

KEY ANALYSIS AREAS:
1. BALANCE CHANGES RECEPTION:
   - Character/Agent/Champion buff/nerf reactions
   - Weapon, item, or ability adjustments feedback
   - Community consensus on whether changes are fair/needed
   - Professional scene impact and adaptation

2. TECHNICAL IMPLEMENTATION:
   - New features, UI changes, or quality of life improvements
   - Performance impacts (FPS, connectivity, stability)
   - Bug reports and issues requiring hotfixes
   - Accessibility or user experience feedback

3. META EVOLUTION:
   - Early predictions on competitive viability changes
   - Strategy shifts and new team compositions
   - Tier list discussions and ranking adjustments
   - Counter-strategy development and adaptation

COMMUNITY SENTIMENT TRACKING:
- Initial reaction sentiment (positive/negative/mixed)
- Most upvoted/discussed changes on Reddit
- Professional player tweet reactions and stream commentary
- Content creator video analysis and community guides
- Official developer response to feedback

REQUIRED REPORTING FORMAT:
1. Patch Version & Release Date: [Exact patch number and timestamp]
2. Community Reception Score: [Positive/Mixed/Negative with rationale]
3. Most Controversial Changes: [Specific changes causing debate]
4. Positive Highlights: [Well-received improvements]
5. Technical Issues: [Bugs, performance problems, or glitches]
6. Meta Predictions: [Early competitive impact assessment]"""

        return QueryEnhancer.enhance_query(base_query, game, timeframe)
