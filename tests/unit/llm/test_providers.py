"""
Tests for LLM provider registry
"""

from unittest.mock import Mock

import pytest

from riot_pulse.llm.base import BaseLLMProvider
from riot_pulse.llm.providers import LLMProviderRegistry


class TestLLMProviderRegistry:
    """Test cases for LLM provider registry"""

    def test_register_provider(self):
        """Test registering a new provider"""
        # Create a mock provider class
        mock_provider_class = Mock()
        mock_provider_class.__name__ = "TestProvider"

        # Register the provider
        LLMProviderRegistry.register("test-provider", mock_provider_class)

        # Verify it was registered
        assert "test-provider" in LLMProviderRegistry._providers
        assert LLMProviderRegistry._providers["test-provider"] == mock_provider_class

    def test_get_provider(self):
        """Test getting a registered provider"""
        # Create a mock provider class that returns a mock instance
        mock_instance = Mock(spec=BaseLLMProvider)
        mock_provider_class = Mock(return_value=mock_instance)
        mock_provider_class.__name__ = "TestProvider"

        # Register the provider
        LLMProviderRegistry.register("test-get", mock_provider_class)

        # Get the provider
        config = {"test": "config"}
        provider = LLMProviderRegistry.get_provider("test-get", config)

        # Verify the provider class was called with config
        mock_provider_class.assert_called_once_with(config)
        assert provider == mock_instance

    def test_get_unknown_provider(self):
        """Test getting an unknown provider raises ValueError"""
        with pytest.raises(ValueError, match="Unknown LLM provider: 'unknown'"):
            LLMProviderRegistry.get_provider("unknown", {})

    def test_list_providers(self):
        """Test listing all registered providers"""
        # Register a test provider
        mock_provider_class = Mock()
        mock_provider_class.__name__ = "ListTestProvider"
        LLMProviderRegistry.register("list-test", mock_provider_class)

        # Get list of providers
        providers = LLMProviderRegistry.list_providers()

        # Verify our test provider is in the list
        assert "list-test" in providers
        assert isinstance(providers, list)
