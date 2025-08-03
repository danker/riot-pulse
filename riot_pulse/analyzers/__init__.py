"""
Analysis modules for different aspects of social listening
"""

from .base import BaseAnalyzer
from .sentiment import SentimentAnalyzer
from .patches import PatchAnalyzer
from .esports import EsportsAnalyzer
from .crisis import CrisisAnalyzer
from .trending import TrendingAnalyzer
from .meta import MetaAnalyzer

from ..config import AnalysisAspects

# Registry of analyzers
_ANALYZER_REGISTRY = {
    AnalysisAspects.SENTIMENT: SentimentAnalyzer,
    AnalysisAspects.PATCHES: PatchAnalyzer,
    AnalysisAspects.ESPORTS: EsportsAnalyzer,
    AnalysisAspects.CRISIS: CrisisAnalyzer,
    AnalysisAspects.TRENDING: TrendingAnalyzer,
    AnalysisAspects.META: MetaAnalyzer,
}


def get_analyzer(aspect: AnalysisAspects) -> BaseAnalyzer:
    """Get analyzer instance for a specific aspect"""
    analyzer_class = _ANALYZER_REGISTRY.get(aspect)
    if not analyzer_class:
        raise ValueError(f"No analyzer found for aspect: {aspect}")
    
    return analyzer_class()


__all__ = [
    "BaseAnalyzer",
    "SentimentAnalyzer", 
    "PatchAnalyzer",
    "EsportsAnalyzer",
    "CrisisAnalyzer",
    "TrendingAnalyzer",
    "MetaAnalyzer",
    "get_analyzer"
]