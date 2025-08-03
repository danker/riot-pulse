"""
OpenAI LLM Provider Adapter
"""

import logging
from typing import Any

from agno.models.openai import OpenAIChat

from ..base import BaseLLMProvider, LLMResponse
from ..providers import LLMProviderRegistry

logger = logging.getLogger(__name__)


class OpenAIAdapter(BaseLLMProvider):
    """Adapter for OpenAI models using Agno framework"""

    def __init__(self, config: dict[str, Any]):
        """
        Initialize OpenAI adapter

        Args:
            config: Configuration dictionary with 'api_key' and optional 'model'
        """
        super().__init__(config)

        # Initialize Agno OpenAI client
        self.client = OpenAIChat(id=self.model, api_key=self.config.get("api_key"))
        logger.info(f"Initialized OpenAI adapter with model: {self.model}")

    def query(self, prompt: str, **kwargs) -> LLMResponse:
        """
        Execute a query against OpenAI

        Args:
            prompt: The prompt/query to send to OpenAI
            **kwargs: Additional parameters (temperature, max_tokens, etc.)

        Returns:
            LLMResponse: Normalized response object
        """
        try:
            logger.debug(f"Querying OpenAI with prompt length: {len(prompt)}")

            # Execute query using Agno
            response = self.client.run(prompt, **kwargs)

            # Extract content from response
            content = self._extract_content(response)

            # Create normalized response
            llm_response = LLMResponse(
                content=content,
                provider="openai",
                model=self.model,
                metadata={
                    "raw_response": response,
                    "response_type": type(response).__name__,
                },
            )

            logger.debug(f"Received response with content length: {len(content)}")
            return llm_response

        except Exception as e:
            logger.error(f"Error querying OpenAI: {e}")
            raise

    def _extract_content(self, response) -> str:
        """
        Extract text content from OpenAI response

        Args:
            response: Raw response from Agno OpenAI

        Returns:
            str: Extracted text content
        """
        # Try different attribute names that Agno might use
        if hasattr(response, "content"):
            return str(response.content)
        elif hasattr(response, "text"):
            return str(response.text)
        elif hasattr(response, "message"):
            return str(response.message)
        elif hasattr(response, "result"):
            return str(response.result)
        elif hasattr(response, "choices") and response.choices:
            # Handle OpenAI API response format
            choice = response.choices[0]
            if hasattr(choice, "message") and hasattr(choice.message, "content"):
                return str(choice.message.content)
            elif hasattr(choice, "text"):
                return str(choice.text)
        else:
            # Fallback to string representation
            logger.warning(
                f"Unknown response structure from OpenAI. "
                f"Response type: {type(response)}, "
                f"attributes: {dir(response)}"
            )
            return str(response)

    def validate_config(self) -> bool:
        """
        Validate OpenAI configuration

        Returns:
            bool: True if configuration is valid

        Raises:
            ValueError: If configuration is invalid
        """
        if not self.config.get("api_key"):
            raise ValueError(
                "OpenAI API key is required. "
                "Set OPENAI_API_KEY environment variable or "
                "provide 'api_key' in configuration."
            )

        # Validate model is supported
        if self.model not in self.supported_models:
            raise ValueError(
                f"Unsupported OpenAI model: {self.model}. "
                f"Supported models: {', '.join(self.supported_models)}"
            )

        return True

    @property
    def name(self) -> str:
        """Provider name"""
        return "openai"

    @property
    def supported_models(self) -> list[str]:
        """List of supported OpenAI models"""
        return [
            "gpt-4",  # GPT-4 base model
            "gpt-4-turbo-preview",  # Latest GPT-4 Turbo (default)
            "gpt-4-turbo",  # GPT-4 Turbo
            "gpt-4o",  # GPT-4 Omni
            "gpt-4o-mini",  # GPT-4 Omni Mini
            "gpt-3.5-turbo",  # GPT-3.5 Turbo
            "gpt-3.5-turbo-16k",  # GPT-3.5 Turbo with 16k context
        ]

    @property
    def default_model(self) -> str:
        """Default model for OpenAI"""
        return "gpt-4-turbo-preview"


# Register the provider
LLMProviderRegistry.register("openai", OpenAIAdapter)
