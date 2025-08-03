"""
xAI LLM Provider Adapter
"""

import logging
from typing import Dict, Any, List

from agno.models.xai import xAI

from ..base import BaseLLMProvider, LLMResponse
from ..providers import LLMProviderRegistry

logger = logging.getLogger(__name__)


class XAIAdapter(BaseLLMProvider):
    """Adapter for xAI Grok models using Agno framework"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize xAI adapter
        
        Args:
            config: Configuration dictionary with 'api_key' and optional 'model'
        """
        super().__init__(config)
        
        # Initialize Agno xAI client
        self.client = xAI(
            id=self.model,
            api_key=self.config.get("api_key")
        )
        logger.info(f"Initialized xAI adapter with model: {self.model}")
    
    def query(self, prompt: str, **kwargs) -> LLMResponse:
        """
        Execute a query against xAI Grok
        
        Args:
            prompt: The prompt/query to send to Grok
            **kwargs: Additional parameters (temperature, max_tokens, etc.)
            
        Returns:
            LLMResponse: Normalized response object
        """
        try:
            logger.debug(f"Querying xAI with prompt length: {len(prompt)}")
            
            # Execute query using Agno
            response = self.client.run(prompt, **kwargs)
            
            # Extract content from response
            content = self._extract_content(response)
            
            # Create normalized response
            llm_response = LLMResponse(
                content=content,
                provider="xai",
                model=self.model,
                metadata={
                    "raw_response": response,
                    "response_type": type(response).__name__
                }
            )
            
            logger.debug(f"Received response with content length: {len(content)}")
            return llm_response
            
        except Exception as e:
            logger.error(f"Error querying xAI: {e}")
            raise
    
    def _extract_content(self, response) -> str:
        """
        Extract text content from xAI response
        
        Args:
            response: Raw response from Agno xAI
            
        Returns:
            str: Extracted text content
        """
        # Try different attribute names that Agno might use
        if hasattr(response, 'content'):
            return str(response.content)
        elif hasattr(response, 'text'):
            return str(response.text)
        elif hasattr(response, 'message'):
            return str(response.message)
        elif hasattr(response, 'result'):
            return str(response.result)
        elif hasattr(response, 'choices') and response.choices:
            # Handle OpenAI-like response format (xAI uses similar structure)
            choice = response.choices[0]
            if hasattr(choice, 'message') and hasattr(choice.message, 'content'):
                return str(choice.message.content)
            elif hasattr(choice, 'text'):
                return str(choice.text)
        else:
            # Fallback to string representation
            logger.warning(
                f"Unknown response structure from xAI. "
                f"Response type: {type(response)}, "
                f"attributes: {dir(response)}"
            )
            return str(response)
    
    def validate_config(self) -> bool:
        """
        Validate xAI configuration
        
        Returns:
            bool: True if configuration is valid
            
        Raises:
            ValueError: If configuration is invalid
        """
        if not self.config.get("api_key"):
            raise ValueError(
                "xAI API key is required. "
                "Set XAI_API_KEY environment variable or "
                "provide 'api_key' in configuration."
            )
        
        # Validate model is supported
        if self.model not in self.supported_models:
            raise ValueError(
                f"Unsupported xAI model: {self.model}. "
                f"Supported models: {', '.join(self.supported_models)}"
            )
        
        return True
    
    @property
    def name(self) -> str:
        """Provider name"""
        return "xai"
    
    @property
    def supported_models(self) -> List[str]:
        """List of supported xAI models"""
        return [
            "grok-1",                   # Grok-1 (current main model, default)
            "grok-beta",                # Grok Beta (experimental features)
        ]
    
    @property
    def default_model(self) -> str:
        """Default model for xAI"""
        return "grok-1"


# Register the provider
LLMProviderRegistry.register("xai", XAIAdapter)