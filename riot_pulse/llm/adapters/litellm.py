"""
LiteLLM Provider Adapter

Provides unified access to 100+ LLM APIs through LiteLLM.
Supports providers like Cohere, Together AI, Replicate, Hugging Face, Groq, and many more.
"""

import logging
from typing import Dict, Any, List

import litellm
from litellm import completion

from ..base import BaseLLMProvider, LLMResponse
from ..providers import LLMProviderRegistry

logger = logging.getLogger(__name__)


class LiteLLMAdapter(BaseLLMProvider):
    """Adapter for LiteLLM unified API supporting 100+ providers"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize LiteLLM adapter
        
        Args:
            config: Configuration dictionary with 'model' and provider-specific settings
        """
        super().__init__(config)
        
        # Configure LiteLLM settings
        litellm.set_verbose = config.get("verbose", False)
        
        # Set up provider-specific API keys from config or environment
        self._setup_api_keys()
        
        logger.info(f"Initialized LiteLLM adapter with model: {self.model}")
    
    def _setup_api_keys(self) -> None:
        """Setup API keys for various providers that LiteLLM supports"""
        # LiteLLM automatically reads from standard environment variables
        # but we can also set them programmatically if provided in config
        
        api_key_mappings = {
            # Core providers
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY", 
            "cohere": "COHERE_API_KEY",
            "replicate": "REPLICATE_API_TOKEN",
            "huggingface": "HUGGINGFACE_API_KEY",
            "together_ai": "TOGETHER_API_KEY",
            "groq": "GROQ_API_KEY",
            "mistral": "MISTRAL_API_KEY",
            "palm": "PALM_API_KEY",
            "gemini": "GEMINI_API_KEY",
            "vertex_ai": "GOOGLE_APPLICATION_CREDENTIALS",
            "bedrock": "AWS_ACCESS_KEY_ID",
            "azure": "AZURE_API_KEY",
            "perplexity": "PERPLEXITY_API_KEY",
        }
        
        # If specific API keys are provided in config, we could set them
        # but LiteLLM typically handles this automatically via environment variables
        if "api_key" in self.config:
            # For cases where a generic api_key is provided
            # LiteLLM will use it appropriately based on the model prefix
            pass
    
    def query(self, prompt: str, **kwargs) -> LLMResponse:
        """
        Execute a query against any LiteLLM-supported provider
        
        Args:
            prompt: The prompt/query to send to the LLM
            **kwargs: Additional parameters (temperature, max_tokens, etc.)
            
        Returns:
            LLMResponse: Normalized response object
        """
        try:
            logger.debug(f"Querying LiteLLM ({self.model}) with prompt length: {len(prompt)}")
            
            # Prepare messages in OpenAI format (LiteLLM standard)
            messages = [{"role": "user", "content": prompt}]
            
            # Merge config parameters with kwargs (kwargs take precedence)
            completion_kwargs = {
                **self.config.get("completion_params", {}),
                **kwargs
            }
            
            # Execute query using LiteLLM
            response = completion(
                model=self.model,
                messages=messages,
                **completion_kwargs
            )
            
            # Extract content from response
            content = self._extract_content(response)
            
            # Extract usage information if available
            usage = None
            if hasattr(response, 'usage') and response.usage:
                usage = {
                    "prompt_tokens": getattr(response.usage, 'prompt_tokens', 0),
                    "completion_tokens": getattr(response.usage, 'completion_tokens', 0),
                    "total_tokens": getattr(response.usage, 'total_tokens', 0),
                }
            
            # Create normalized response
            llm_response = LLMResponse(
                content=content,
                provider="litellm",
                model=self.model,
                usage=usage,
                metadata={
                    "raw_response": response,
                    "actual_provider": self._get_provider_from_model(self.model),
                    "response_type": type(response).__name__
                }
            )
            
            logger.debug(f"Received response with content length: {len(content)}")
            return llm_response
            
        except Exception as e:
            logger.error(f"Error querying LiteLLM ({self.model}): {e}")
            raise
    
    def _extract_content(self, response) -> str:
        """
        Extract text content from LiteLLM response
        
        Args:
            response: Raw response from LiteLLM
            
        Returns:
            str: Extracted text content
        """
        try:
            # LiteLLM returns OpenAI-compatible response format
            if hasattr(response, 'choices') and response.choices:
                choice = response.choices[0]
                if hasattr(choice, 'message') and hasattr(choice.message, 'content'):
                    return str(choice.message.content)
                elif hasattr(choice, 'text'):
                    return str(choice.text)
            
            # Fallback attempts
            if hasattr(response, 'content'):
                return str(response.content)
            elif hasattr(response, 'text'):
                return str(response.text)
            else:
                logger.warning(
                    f"Unknown response structure from LiteLLM. "
                    f"Response type: {type(response)}, "
                    f"attributes: {dir(response)}"
                )
                return str(response)
                
        except Exception as e:
            logger.error(f"Error extracting content from LiteLLM response: {e}")
            return str(response)
    
    def _get_provider_from_model(self, model: str) -> str:
        """
        Extract the actual provider from the model string
        
        Args:
            model: Model string (e.g., "claude-3-sonnet", "gemini/gemini-pro")
            
        Returns:
            str: Provider name
        """
        if "/" in model:
            return model.split("/")[0]
        elif model.startswith("claude"):
            return "anthropic"
        elif model.startswith("gpt"):
            return "openai"
        elif model.startswith("gemini"):
            return "google"
        elif model.startswith("command"):
            return "cohere"
        else:
            return "unknown"
    
    def validate_config(self) -> bool:
        """
        Validate LiteLLM configuration
        
        Returns:
            bool: True if configuration is valid
            
        Raises:
            ValueError: If configuration is invalid
        """
        if not self.config.get("model"):
            raise ValueError(
                "LiteLLM model is required. "
                "Specify model in configuration (e.g., 'claude-3-sonnet', 'gemini/gemini-pro')."
            )
        
        # Validate model format
        model = self.model
        if not model:
            raise ValueError("Model cannot be empty")
        
        # Check if it's a known supported model pattern
        supported_prefixes = [
            "claude", "gpt", "gemini", "command", "together_ai", "replicate",
            "huggingface", "groq", "mistral", "palm", "bedrock", "azure",
            "vertex_ai", "cohere", "perplexity"
        ]
        
        is_supported = any(
            model.startswith(prefix) or f"/{prefix}" in model.lower() 
            for prefix in supported_prefixes
        )
        
        if not is_supported:
            logger.warning(
                f"Model '{model}' may not be supported by LiteLLM. "
                f"Please verify the model format. "
                f"See https://docs.litellm.ai/docs/providers for supported models."
            )
        
        return True
    
    @property
    def name(self) -> str:
        """Provider name"""
        return "litellm"
    
    @property
    def supported_models(self) -> List[str]:
        """List of example supported models (LiteLLM supports 100+ models)"""
        return [
            # Anthropic
            "claude-3-5-sonnet-20241022",
            "claude-3-opus-20240229", 
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307",
            
            # OpenAI
            "gpt-4o",
            "gpt-4-turbo",
            "gpt-4",
            "gpt-3.5-turbo",
            
            # Google
            "gemini/gemini-pro",
            "gemini/gemini-pro-vision", 
            "vertex_ai/gemini-pro",
            
            # Cohere
            "command-r-plus",
            "command-r",
            "command",
            
            # Together AI
            "together_ai/meta-llama/Llama-2-70b-chat-hf",
            "together_ai/meta-llama/Llama-2-13b-chat-hf",
            "together_ai/mistralai/Mixtral-8x7B-Instruct-v0.1",
            
            # Groq
            "groq/llama2-70b-4096",
            "groq/mixtral-8x7b-32768",
            
            # Replicate
            "replicate/meta/llama-2-70b-chat:latest",
            "replicate/mistralai/mixtral-8x7b-instruct-v0.1",
            
            # Perplexity
            "perplexity/llama-3.1-sonar-large-128k-online",
            "perplexity/llama-3.1-sonar-small-128k-online",
        ]
    
    @property
    def default_model(self) -> str:
        """Default model for LiteLLM"""
        return "claude-3-5-sonnet-20241022"


# Register the provider
LLMProviderRegistry.register("litellm", LiteLLMAdapter)