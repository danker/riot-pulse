"""
Base interface for LLM providers
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class LLMResponse:
    """Normalized response format across all providers"""

    content: str
    provider: str
    model: str
    usage: dict[str, int] | None = None
    metadata: dict[str, Any] | None = None

    def __str__(self) -> str:
        """String representation returns just the content"""
        return self.content


class BaseLLMProvider(ABC):
    """Base interface for all LLM providers"""

    def __init__(self, config: dict[str, Any]):
        """
        Initialize the provider with configuration

        Args:
            config: Provider-specific configuration dictionary
        """
        self.config = config
        self._validate_config()

    @abstractmethod
    def query(self, prompt: str, **kwargs) -> LLMResponse:
        """
        Execute a query against the LLM

        Args:
            prompt: The prompt/query to send to the LLM
            **kwargs: Additional provider-specific parameters

        Returns:
            LLMResponse: Normalized response object
        """
        pass

    @abstractmethod
    def validate_config(self) -> bool:
        """
        Validate provider configuration

        Returns:
            bool: True if configuration is valid

        Raises:
            ValueError: If configuration is invalid
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Provider name"""
        pass

    @property
    @abstractmethod
    def supported_models(self) -> list[str]:
        """List of supported models"""
        pass

    @property
    def model(self) -> str:
        """Currently configured model"""
        return self.config.get("model", self.default_model)

    @property
    @abstractmethod
    def default_model(self) -> str:
        """Default model for this provider"""
        pass

    def _validate_config(self) -> None:
        """Internal configuration validation"""
        if not self.validate_config():
            raise ValueError(f"Invalid configuration for {self.name} provider")

    def __repr__(self) -> str:
        """String representation of the provider"""
        return f"{self.__class__.__name__}(model={self.model})"
