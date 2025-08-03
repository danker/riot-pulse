"""
LLM Provider Registry and Factory
"""

import logging
from typing import Any

from .base import BaseLLMProvider
from .config import LLMConfig

logger = logging.getLogger(__name__)


class LLMProviderRegistry:
    """Registry for LLM providers"""

    _providers: dict[str, type[BaseLLMProvider]] = {}

    @classmethod
    def register(cls, name: str, provider_class: type[BaseLLMProvider]) -> None:
        """
        Register a new LLM provider

        Args:
            name: Provider name (e.g., 'perplexity', 'openai')
            provider_class: Provider class implementing BaseLLMProvider
        """
        logger.debug(f"Registering LLM provider: {name}")
        cls._providers[name.lower()] = provider_class

    @classmethod
    def get_provider(cls, name: str, config: dict[str, Any]) -> BaseLLMProvider:
        """
        Get an instance of the specified provider

        Args:
            name: Provider name
            config: Provider configuration

        Returns:
            BaseLLMProvider: Configured provider instance

        Raises:
            ValueError: If provider is not registered
        """
        provider_name = name.lower()
        if provider_name not in cls._providers:
            available = ", ".join(cls._providers.keys())
            raise ValueError(
                f"Unknown LLM provider: '{name}'. Available providers: {available}"
            )

        logger.info(f"Creating LLM provider: {provider_name}")
        return cls._providers[provider_name](config)

    @classmethod
    def list_providers(cls) -> list[str]:
        """Get list of registered provider names"""
        return list(cls._providers.keys())


def get_llm_provider(
    config_file: str | None = None,
    provider_override: str | None = None,
    model_override: str | None = None,
) -> BaseLLMProvider:
    """
    Get configured LLM provider instance

    This is the main entry point for getting an LLM provider.
    Configuration priority: CLI args > Environment > Config file

    Args:
        config_file: Path to configuration file (default: config.yaml)
        provider_override: Override provider from CLI
        model_override: Override model from CLI

    Returns:
        BaseLLMProvider: Configured provider instance
    """
    # Load configuration
    llm_config = LLMConfig(config_file or "config.yaml")
    provider_config = llm_config.get_provider_config()

    # Apply CLI overrides
    if provider_override:
        provider_config["name"] = provider_override
        # Get the specific provider config if it exists
        provider_specific = llm_config.config.get("llm", {}).get(provider_override, {})
        provider_config["config"].update(provider_specific)

    if model_override:
        provider_config["config"]["model"] = model_override

    # Get provider instance
    provider = LLMProviderRegistry.get_provider(
        provider_config["name"], provider_config["config"]
    )

    logger.info(f"Initialized {provider.name} provider with model: {provider.model}")

    return provider


# Import adapters to trigger registration
def _load_adapters():
    """Load all available adapters"""
    try:
        from .adapters import perplexity

        logger.debug("Loaded Perplexity adapter")
    except ImportError as e:
        logger.warning(f"Could not load Perplexity adapter: {e}")

    try:
        from .adapters import openai

        logger.debug("Loaded OpenAI adapter")
    except ImportError as e:
        logger.debug(f"Could not load OpenAI adapter: {e}")

    try:
        from .adapters import anthropic

        logger.debug("Loaded Anthropic adapter")
    except ImportError as e:
        logger.debug(f"Could not load Anthropic adapter: {e}")

    try:
        from .adapters import xai

        logger.debug("Loaded xAI adapter")
    except ImportError as e:
        logger.debug(f"Could not load xAI adapter: {e}")


# Load adapters when module is imported
_load_adapters()
