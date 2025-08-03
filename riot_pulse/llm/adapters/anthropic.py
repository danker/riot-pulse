"""
Anthropic LLM Provider Adapter
"""

import logging
from typing import Dict, Any, List

from agno.models.anthropic import Claude

from ..base import BaseLLMProvider, LLMResponse
from ..providers import LLMProviderRegistry

logger = logging.getLogger(__name__)


class AnthropicAdapter(BaseLLMProvider):
    """Adapter for Anthropic Claude models using Agno framework"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Anthropic adapter
        
        Args:
            config: Configuration dictionary with 'api_key' and optional 'model'
        """
        super().__init__(config)
        
        # Initialize Agno Anthropic client
        self.client = Claude(
            id=self.model,
            api_key=self.config.get("api_key")
        )
        logger.info(f"Initialized Anthropic adapter with model: {self.model}")
    
    def query(self, prompt: str, **kwargs) -> LLMResponse:
        """
        Execute a query against Anthropic Claude
        
        Args:
            prompt: The prompt/query to send to Claude
            **kwargs: Additional parameters (temperature, max_tokens, etc.)
            
        Returns:
            LLMResponse: Normalized response object
        """
        try:
            logger.debug(f"Querying Anthropic with prompt length: {len(prompt)}")
            
            # Execute query using Agno
            response = self.client.run(prompt, **kwargs)
            
            # Extract content from response
            content = self._extract_content(response)
            
            # Create normalized response
            llm_response = LLMResponse(
                content=content,
                provider="anthropic",
                model=self.model,
                metadata={
                    "raw_response": response,
                    "response_type": type(response).__name__
                }
            )
            
            logger.debug(f"Received response with content length: {len(content)}")
            return llm_response
            
        except Exception as e:
            logger.error(f"Error querying Anthropic: {e}")
            raise
    
    def _extract_content(self, response) -> str:
        """
        Extract text content from Anthropic response
        
        Args:
            response: Raw response from Agno Anthropic
            
        Returns:
            str: Extracted text content
        """
        # Try different attribute names that Agno might use
        if hasattr(response, 'content'):
            # Handle both string content and list of content blocks
            content = response.content
            if isinstance(content, list) and len(content) > 0:
                # Extract text from content blocks
                if hasattr(content[0], 'text'):
                    return str(content[0].text)
                else:
                    return str(content[0])
            return str(content)
        elif hasattr(response, 'text'):
            return str(response.text)
        elif hasattr(response, 'message'):
            return str(response.message)
        elif hasattr(response, 'result'):
            return str(response.result)
        else:
            # Fallback to string representation
            logger.warning(
                f"Unknown response structure from Anthropic. "
                f"Response type: {type(response)}, "
                f"attributes: {dir(response)}"
            )
            return str(response)
    
    def validate_config(self) -> bool:
        """
        Validate Anthropic configuration
        
        Returns:
            bool: True if configuration is valid
            
        Raises:
            ValueError: If configuration is invalid
        """
        if not self.config.get("api_key"):
            raise ValueError(
                "Anthropic API key is required. "
                "Set ANTHROPIC_API_KEY environment variable or "
                "provide 'api_key' in configuration."
            )
        
        # Validate model is supported
        if self.model not in self.supported_models:
            raise ValueError(
                f"Unsupported Anthropic model: {self.model}. "
                f"Supported models: {', '.join(self.supported_models)}"
            )
        
        return True
    
    @property
    def name(self) -> str:
        """Provider name"""
        return "anthropic"
    
    @property
    def supported_models(self) -> List[str]:
        """List of supported Anthropic models"""
        return [
            "claude-3-opus-20240229",       # Claude 3 Opus (most capable, default)
            "claude-3-sonnet-20240229",     # Claude 3 Sonnet (balanced)
            "claude-3-haiku-20240307",      # Claude 3 Haiku (fastest)
            "claude-3-5-sonnet-20241022",   # Claude 3.5 Sonnet (latest)
            "claude-3-5-haiku-20241022",    # Claude 3.5 Haiku (latest fast)
        ]
    
    @property
    def default_model(self) -> str:
        """Default model for Anthropic"""
        return "claude-3-opus-20240229"


# Register the provider
LLMProviderRegistry.register("anthropic", AnthropicAdapter)