"""
Core Riot Games Social Listening Agent
"""

import os
from typing import Dict, Any
from agno.agent import Agent
from agno.models.perplexity import Perplexity
from dotenv import load_dotenv

from ..config import RiotGames, AnalysisAspects, PERPLEXITY_CONFIG
from ..analyzers import get_analyzer

# Load environment variables
load_dotenv()


class RiotSocialListenerAgent(Agent):
    """Main agent for Riot Games social listening"""
    
    def __init__(self, perplexity_api_key: str = None):
        # Get API key from environment if not provided
        if perplexity_api_key is None:
            perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")
            if not perplexity_api_key:
                raise ValueError("PERPLEXITY_API_KEY environment variable is required")
        
        # Initialize the agent with Perplexity model
        super().__init__(
            name="Riot Games Social Listening Agent",
            model=Perplexity(id=PERPLEXITY_CONFIG["model_id"], api_key=perplexity_api_key),
            description="Monitors community sentiment and trends across all Riot Games titles",
            instructions=PERPLEXITY_CONFIG["instructions"],
            markdown=True
        )
    
    def analyze_game_aspect(
        self, 
        game: RiotGames, 
        aspect: AnalysisAspects, 
        timeframe: str = "24 hours"
    ) -> str:
        """
        Analyze a specific aspect for a specific game
        
        Args:
            game: The Riot game to analyze
            aspect: The analysis aspect to perform
            timeframe: Time period to analyze
            
        Returns:
            Analysis results as formatted text
        """
        analyzer = get_analyzer(aspect)
        query = analyzer.generate_query(game, timeframe)
        
        # Run the analysis using the agent
        response = self.run(query)
        return response
    
    def get_game_display_name(self, game: RiotGames) -> str:
        """Get display name for a game"""
        return RiotGames.get_display_name(game)
    
    def get_aspect_display_name(self, aspect: AnalysisAspects) -> str:
        """Get display name for an analysis aspect"""
        return AnalysisAspects.get_display_name(aspect)