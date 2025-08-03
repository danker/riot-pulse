"""
Riot Pulse - AI-powered social listening for Riot Games communities
"""

__version__ = "0.1.0"
__author__ = "Riot Pulse Team"
__description__ = "AI-powered social listening platform for Riot Games communities"

from .agents.social_listener import RiotSocialListenerAgent
from .config import AnalysisAspects, RiotGames

__all__ = ["RiotGames", "AnalysisAspects", "RiotSocialListenerAgent"]
