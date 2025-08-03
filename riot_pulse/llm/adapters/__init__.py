"""
LLM Provider Adapters

Each adapter implements the BaseLLMProvider interface for a specific LLM service.
Adapters are automatically registered when imported.
"""

# Import available adapters to trigger registration
__all__ = []

# Try to import each adapter - failures are okay since not all may be implemented yet
try:
    from . import perplexity

    __all__.append("perplexity")
except ImportError:
    pass

try:
    from . import openai

    __all__.append("openai")
except ImportError:
    pass

try:
    from . import anthropic

    __all__.append("anthropic")
except ImportError:
    pass

try:
    from . import xai

    __all__.append("xai")
except ImportError:
    pass

try:
    from . import litellm

    __all__.append("litellm")
except ImportError:
    pass
