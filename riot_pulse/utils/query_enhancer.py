"""
Query enhancement utilities for better Perplexity results
"""

from datetime import datetime, timedelta
from typing import List, Dict
from ..config import RiotGames


class QueryEnhancer:
    """Enhances queries for better temporal accuracy and source quality"""
    
    # Trusted gaming sources ranked by reliability
    TRUSTED_SOURCES = {
        "tier_1": [
            "reddit.com",
            "riotgames.com", 
            "lolesports.com",
            "valorant-esports.com"
        ],
        "tier_2": [
            "dotesports.com",
            "gamespot.com",
            "ign.com",
            "polygon.com",
            "theverge.com",
            "kotaku.com"
        ],
        "tier_3": [
            "twitter.com",
            "youtube.com",
            "twitch.tv",
            "dexerto.com",
            "sportskeeda.com"
        ]
    }
    
    @classmethod
    def get_temporal_constraints(cls, timeframe: str) -> Dict[str, str]:
        """Convert timeframe to specific date constraints"""
        now = datetime.now()
        
        # Parse common timeframe formats
        if "24 hours" in timeframe or "1 day" in timeframe:
            cutoff = now - timedelta(days=1)
            strict_timeframe = "within the last 24 hours"
            date_constraint = f"after {cutoff.strftime('%B %d, %Y')}"
        elif "48 hours" in timeframe or "2 days" in timeframe:
            cutoff = now - timedelta(days=2)
            strict_timeframe = "within the last 48 hours"
            date_constraint = f"after {cutoff.strftime('%B %d, %Y')}"
        elif "1 week" in timeframe or "7 days" in timeframe:
            cutoff = now - timedelta(days=7)
            strict_timeframe = "within the last week"
            date_constraint = f"after {cutoff.strftime('%B %d, %Y')}"
        elif "1 month" in timeframe or "30 days" in timeframe:
            cutoff = now - timedelta(days=30)
            strict_timeframe = "within the last month"
            date_constraint = f"after {cutoff.strftime('%B %d, %Y')}"
        else:
            # Default to 24 hours
            cutoff = now - timedelta(days=1)
            strict_timeframe = "within the last 24 hours"
            date_constraint = f"after {cutoff.strftime('%B %d, %Y')}"
        
        return {
            "strict_timeframe": strict_timeframe,
            "date_constraint": date_constraint,
            "exact_cutoff": cutoff.strftime('%Y-%m-%d')
        }
    
    @classmethod
    def get_source_bias_instruction(cls) -> str:
        """Generate source prioritization instructions"""
        all_sources = []
        for tier_sources in cls.TRUSTED_SOURCES.values():
            all_sources.extend(tier_sources)
        
        return f"""
CRITICAL SOURCE REQUIREMENTS:
- ONLY use sources from the following trusted domains: {', '.join(all_sources[:8])}
- PRIORITIZE Reddit threads, official Riot sources, and established gaming news sites
- REJECT results from: random blogs, personal websites, unverified social media accounts
- Each source URL must be from a recognized gaming publication or official community
"""
    
    @classmethod
    def get_temporal_enforcement(cls, temporal_info: Dict[str, str]) -> str:
        """Generate strict temporal enforcement instructions"""
        return f"""
CRITICAL TEMPORAL REQUIREMENTS:
- ONLY include content published {temporal_info['strict_timeframe']}
- REJECT any sources older than {temporal_info['date_constraint']}
- If no recent content exists for this timeframe, state "No recent activity found"
- Verify publication dates - sources must be from {temporal_info['exact_cutoff']} or later
- Do not include older content even if it seems relevant
"""
    
    @classmethod
    def get_game_specific_sources(cls, game: RiotGames) -> List[str]:
        """Get game-specific subreddits and communities"""
        game_sources = {
            RiotGames.VALORANT: [
                "r/VALORANT",
                "r/ValorantCompetitive", 
                "r/AgentAcademy"
            ],
            RiotGames.LEAGUE_OF_LEGENDS: [
                "r/leagueoflegends",
                "r/summonerschool",
                "r/CompetitiveLoL"
            ],
            RiotGames.TEAMFIGHT_TACTICS: [
                "r/TeamfightTactics",
                "r/CompetitiveTFT"
            ],
            RiotGames.LEGENDS_OF_RUNETERRA: [
                "r/LegendsOfRuneterra",
                "r/LoRCompetitive"
            ],
            RiotGames.TWOXKO: [
                "r/2XKO",
                "r/FightingGames"
            ],
            RiotGames.RIFTBOUND: [
                "r/LeagueOfLegends",
                "r/tabletopgaming"
            ]
        }
        
        return game_sources.get(game, ["r/RiotGames"])
    
    @classmethod
    def enhance_query(cls, base_query: str, game: RiotGames, timeframe: str) -> str:
        """Enhance a query with temporal and source constraints"""
        temporal_info = cls.get_temporal_constraints(timeframe)
        source_bias = cls.get_source_bias_instruction()
        temporal_enforcement = cls.get_temporal_enforcement(temporal_info)
        game_sources = cls.get_game_specific_sources(game)
        
        enhanced_query = f"""
{base_query}

{source_bias}

{temporal_enforcement}

SPECIFIC COMMUNITIES TO CHECK:
- {', '.join(game_sources)}
- Official Riot Games social media and announcements
- Verified content creator channels and streams

SEARCH METHODOLOGY:
1. Search with date filters for {temporal_info['strict_timeframe']}
2. Prioritize Reddit posts and comments from game-specific subreddits
3. Check official Riot announcements and developer updates
4. Include only verified gaming news publications
5. Cross-reference multiple sources for accuracy

RESPONSE REQUIREMENTS:
- Include exact timestamps for all sources
- Verify all URLs are from trusted domains
- If insufficient recent content exists, clearly state the limitation
- Focus on factual reporting over speculation
"""
        
        return enhanced_query.strip()