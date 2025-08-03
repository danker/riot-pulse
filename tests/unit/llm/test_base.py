"""
Tests for LLM base classes and interfaces
"""

import pytest

from riot_pulse.llm.base import BaseLLMProvider, LLMResponse


class TestLLMResponse:
    """Test cases for LLMResponse dataclass"""

    def test_str_representation(self, sample_llm_response: LLMResponse):
        """Test that string representation returns content"""
        assert str(sample_llm_response) == sample_llm_response.content

    def test_response_creation(self):
        """Test basic response creation"""
        response = LLMResponse(
            content="Test content", provider="test", model="test-model"
        )

        assert response.content == "Test content"
        assert response.provider == "test"
        assert response.model == "test-model"
        assert response.usage is None
        assert response.metadata is None

    def test_response_with_usage_and_metadata(self):
        """Test response creation with usage and metadata"""
        usage = {"prompt_tokens": 5, "completion_tokens": 10}
        metadata = {"temperature": 0.8}

        response = LLMResponse(
            content="Test content",
            provider="test",
            model="test-model",
            usage=usage,
            metadata=metadata,
        )

        assert response.usage == usage
        assert response.metadata == metadata


class TestBaseLLMProvider:
    """Test cases for BaseLLMProvider interface"""

    def test_provider_is_abstract(self):
        """Test that BaseLLMProvider cannot be instantiated directly"""
        with pytest.raises(TypeError):
            BaseLLMProvider({"test": "config"})  # type: ignore

    def test_mock_provider_interface(self, mock_llm_provider):
        """Test that mock provider implements required interface"""
        # Test properties
        assert hasattr(mock_llm_provider, "name")
        assert hasattr(mock_llm_provider, "model")
        assert hasattr(mock_llm_provider, "supported_models")
        assert hasattr(mock_llm_provider, "default_model")

        # Test methods
        assert hasattr(mock_llm_provider, "query")
        assert hasattr(mock_llm_provider, "validate_config")

        # Test method calls
        response = mock_llm_provider.query("test prompt")
        assert isinstance(response, LLMResponse)
        assert response.content == "Test response from mock provider"

        assert mock_llm_provider.validate_config() is True
