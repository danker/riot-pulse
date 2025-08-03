"""
Riot Pulse - AI-powered social listening for Riot Games communities
"""

__version__ = "0.1.0"
__author__ = "Riot Pulse Team"
__description__ = "AI-powered social listening platform for Riot Games communities"

from .config import RiotGames, AnalysisAspects
from .agents.social_listener import RiotSocialListenerAgent

__all__ = [
    "RiotGames",
    "AnalysisAspects", 
    "RiotSocialListenerAgent"
]