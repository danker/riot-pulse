"""
Pytest configuration and shared fixtures
"""

from typing import Any
from unittest.mock import Mock

import pytest

from riot_pulse.llm.base import BaseLLMProvider, LLMResponse


@pytest.fixture
def mock_llm_config() -> dict[str, Any]:
    """Mock LLM configuration for testing"""
    return {
        "api_key": "test-api-key",
        "model": "test-model",
    }


@pytest.fixture
def mock_llm_provider(mock_llm_config: dict[str, Any]) -> Mock:
    """Mock LLM provider for testing"""
    provider = Mock(spec=BaseLLMProvider)
    provider.name = "test"
    provider.model = "test-model"
    provider.config = mock_llm_config
    provider.validate_config.return_value = True
    provider.supported_models = ["test-model", "test-model-2"]
    provider.default_model = "test-model"

    # Mock query method to return a sample response
    mock_response = LLMResponse(
        content="Test response from mock provider",
        provider="test",
        model="test-model",
        metadata={"mock": True},
    )
    provider.query.return_value = mock_response

    return provider


@pytest.fixture
def sample_llm_response() -> LLMResponse:
    """Sample LLM response for testing"""
    return LLMResponse(
        content="This is a test response from an LLM provider.",
        provider="test-provider",
        model="test-model-v1",
        usage={"prompt_tokens": 10, "completion_tokens": 15, "total_tokens": 25},
        metadata={"temperature": 0.7, "max_tokens": 100},
    )


@pytest.fixture
def sample_prompt() -> str:
    """Sample prompt for testing"""
    return "What is League of Legends? Provide a brief explanation."
