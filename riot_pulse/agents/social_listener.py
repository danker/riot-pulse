"""
Core Riot Games Social Listening Agent
"""

import os
from typing import Dict, Any, Optional
from agno.agent import Agent
from dotenv import load_dotenv

from ..config import RiotGames, AnalysisAspects, PERPLEXITY_CONFIG
from ..analyzers import get_analyzer
from ..llm import get_llm_provider, BaseLLMProvider

# Load environment variables
load_dotenv()


class RiotSocialListenerAgent(Agent):
    """Main agent for Riot Games social listening"""
    
    def __init__(self, 
                 llm_provider: Optional[BaseLLMProvider] = None,
                 config_file: Optional[str] = None,
                 provider_override: Optional[str] = None,
                 model_override: Optional[str] = None):
        """
        Initialize the social listening agent
        
        Args:
            llm_provider: Pre-configured LLM provider (optional)
            config_file: Path to configuration file (optional)
            provider_override: Override provider from config (optional)
            model_override: Override model from config (optional)
        """
        # Get LLM provider
        if llm_provider:
            self.llm_provider = llm_provider
        else:
            self.llm_provider = get_llm_provider(
                config_file=config_file,
                provider_override=provider_override,
                model_override=model_override
            )
        
        # For backward compatibility with Agno Agent, use the Agno model if it's Perplexity
        # Otherwise, we'll override the run method
        if self.llm_provider.name == "perplexity" and hasattr(self.llm_provider, 'client'):
            model = self.llm_provider.client
        else:
            # Use a dummy model for non-Perplexity providers
            # We'll override the run method to use our provider
            model = None
        
        # Initialize the agent
        super().__init__(
            name="Riot Games Social Listening Agent",
            model=model,
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
        
        # Use our LLM provider directly
        response = self.llm_provider.query(query)
        
        # Return the content string
        return response.content
    
    def get_game_display_name(self, game: RiotGames) -> str:
        """Get display name for a game"""
        return RiotGames.get_display_name(game)
    
    def get_aspect_display_name(self, aspect: AnalysisAspects) -> str:
        """Get display name for an analysis aspect"""
        return AnalysisAspects.get_display_name(aspect)