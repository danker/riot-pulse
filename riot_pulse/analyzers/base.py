"""
Base analyzer interface for all analysis aspects
"""

from abc import ABC, abstractmethod
from ..config import RiotGames


class BaseAnalyzer(ABC):
    """Base class for all analysis aspects"""
    
    @abstractmethod
    def generate_query(self, game: RiotGames, timeframe: str = "24 hours") -> str:
        """
        Generate a query for this analysis aspect
        
        Args:
            game: The Riot game to analyze
            timeframe: Time period to analyze
            
        Returns:
            Query string for the Perplexity model
        """
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable name for this analyzer"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Description of what this analyzer does"""
        pass