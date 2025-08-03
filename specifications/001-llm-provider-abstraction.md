# Specification: LLM Provider Abstraction

**Spec ID:** 001-llm-provider-abstraction  
**Author:** Claude (with edanker)  
**Date:** 2024-12-04  
**Status:** In Review

## 1. Problem Statement

The current implementation is tightly coupled to Perplexity as the LLM provider. This creates several issues:
- Cannot easily switch between providers when Perplexity's quality is unsatisfactory
- No ability to compare responses across different LLMs
- Difficult to test with different models or providers
- No fallback options when a provider is unavailable
- Hard-coded provider-specific logic throughout the codebase

## 2. Goals & Requirements

### Primary Goals
- Create a provider-agnostic LLM interface
- Enable easy switching between LLM providers via configuration
- Maintain consistent response format across all providers
- Leverage Agno framework's existing model support

### Requirements
- **Must Have:**
  - Support for Perplexity (current), OpenAI, Anthropic, and xAI initially
  - Configuration-based provider selection (YAML → ENV → CLI priority)
  - Consistent response format across providers
  - Provider-specific API key management
  - Clear error messages for misconfiguration
  - Zero breaking changes to existing functionality
- **Should Have:**
  - Dry-run mode for testing configuration
  - Response quality benchmarking tool
  - Provider feature compatibility matrix
  - Response time and performance metrics
- **Nice to Have:**
  - Cost estimation per provider (future enhancement)
  - Automatic provider health checks
  - Response caching layer

### Non-Goals
- Multi-provider fallback chains (fail fast approach)
- Context window management (defer to later)
- Streaming response support (not needed for current use case)

## 3. Technical Design

### Architecture Overview

```
┌─────────────────────┐     ┌──────────────────┐
│ RiotSocialListener  │────▶│  LLMProvider     │
│      Agent          │     │   (Interface)    │
└─────────────────────┘     └──────────────────┘
                                     │
                ┌────────────────────┼────────────────────┐
                ▼                    ▼                    ▼
       ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
       │ PerplexityAdapter│ │  OpenAIAdapter   │ │ AnthropicAdapter │
       └──────────────────┘ └──────────────────┘ └──────────────────┘
                │                    │                    │
                ▼                    ▼                    ▼
       ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
       │ Agno Perplexity  │ │  Agno OpenAI     │ │ Agno Anthropic   │
       └──────────────────┘ └──────────────────┘ └──────────────────┘
```

### Detailed Design

#### 1. Base Provider Interface (`riot_pulse/llm/base.py`)
```python
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class LLMResponse:
    """Normalized response format across all providers"""
    content: str
    provider: str
    model: str
    usage: Optional[Dict[str, int]] = None
    metadata: Optional[Dict[str, Any]] = None

class BaseLLMProvider(ABC):
    """Base interface for all LLM providers"""
    
    @abstractmethod
    def __init__(self, config: Dict[str, Any]):
        pass
    
    @abstractmethod
    def query(self, prompt: str, **kwargs) -> LLMResponse:
        """Execute a query against the LLM"""
        pass
    
    @abstractmethod
    def validate_config(self) -> bool:
        """Validate provider configuration"""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Provider name"""
        pass
    
    @property
    @abstractmethod
    def supported_models(self) -> List[str]:
        """List of supported models"""
        pass
```

#### 2. Provider Registry (`riot_pulse/llm/providers.py`)
```python
from typing import Dict, Type
from .base import BaseLLMProvider

class LLMProviderRegistry:
    """Registry for LLM providers"""
    _providers: Dict[str, Type[BaseLLMProvider]] = {}
    
    @classmethod
    def register(cls, name: str, provider_class: Type[BaseLLMProvider]):
        cls._providers[name] = provider_class
    
    @classmethod
    def get_provider(cls, name: str, config: Dict[str, Any]) -> BaseLLMProvider:
        if name not in cls._providers:
            raise ValueError(f"Unknown provider: {name}")
        return cls._providers[name](config)
```

#### 3. Configuration System (`riot_pulse/llm/config.py`)
```python
import yaml
import os
from typing import Dict, Any, Optional

class LLMConfig:
    """Manages LLM provider configuration"""
    
    def __init__(self, config_file: str = "config.yaml"):
        self.config = self._load_config(config_file)
    
    def _load_config(self, config_file: str) -> Dict[str, Any]:
        # Priority: YAML → ENV → CLI
        config = {}
        
        # 1. Load from YAML
        if os.path.exists(config_file):
            with open(config_file) as f:
                config = yaml.safe_load(f)
        
        # 2. Override with environment variables
        provider = os.getenv("LLM_PROVIDER")
        if provider:
            config["provider"] = provider
        
        # 3. CLI overrides handled by caller
        
        return config
    
    def get_provider_config(self) -> Dict[str, Any]:
        provider_name = self.config.get("llm", {}).get("provider", "perplexity")
        provider_config = self.config.get("llm", {}).get(provider_name, {})
        
        # Add API keys from environment
        api_key_env = f"{provider_name.upper()}_API_KEY"
        if os.getenv(api_key_env):
            provider_config["api_key"] = os.getenv(api_key_env)
        
        return {
            "name": provider_name,
            "config": provider_config
        }
```

#### 4. Example Adapter (`riot_pulse/llm/adapters/perplexity.py`)
```python
from agno.models.perplexity import Perplexity
from ..base import BaseLLMProvider, LLMResponse
from ..providers import LLMProviderRegistry

class PerplexityAdapter(BaseLLMProvider):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.client = Perplexity(
            id=config.get("model", "sonar-pro"),
            api_key=config.get("api_key")
        )
    
    def query(self, prompt: str, **kwargs) -> LLMResponse:
        response = self.client.run(prompt, **kwargs)
        
        # Normalize response
        return LLMResponse(
            content=response.content if hasattr(response, 'content') else str(response),
            provider="perplexity",
            model=self.config.get("model", "sonar-pro"),
            metadata={"raw_response": response}
        )
    
    def validate_config(self) -> bool:
        return bool(self.config.get("api_key"))
    
    @property
    def name(self) -> str:
        return "perplexity"
    
    @property
    def supported_models(self) -> List[str]:
        return ["sonar", "sonar-pro", "sonar-reasoning"]

# Register the provider
LLMProviderRegistry.register("perplexity", PerplexityAdapter)
```

### Configuration File Format (`config.yaml`)
```yaml
llm:
  provider: perplexity  # Can be: perplexity, openai, anthropic, xai
  
  perplexity:
    model: sonar-pro
    # api_key comes from PERPLEXITY_API_KEY env var
    
  openai:
    model: gpt-4-turbo-preview
    # api_key comes from OPENAI_API_KEY env var
    
  anthropic:
    model: claude-3-opus-20240229
    # api_key comes from ANTHROPIC_API_KEY env var
    
  xai:
    model: grok-1
    # api_key comes from XAI_API_KEY env var

# Rest of configuration...
```

## 4. Implementation Plan

### Phase 1: Core Infrastructure
- [x] Create specifications directory and template
- [ ] Create LLM package structure (`riot_pulse/llm/`)
- [ ] Implement base provider interface
- [ ] Create provider registry system
- [ ] Implement configuration loader

### Phase 2: Provider Adapters
- [ ] Create Perplexity adapter (maintain current functionality)
- [ ] Add OpenAI adapter
- [ ] Add Anthropic adapter
- [ ] Add xAI adapter
- [ ] Implement response normalization

### Phase 3: Integration
- [ ] Update RiotSocialListenerAgent to use new abstraction
- [ ] Add config.yaml to project
- [ ] Update CLI to support --llm-provider flag
- [ ] Update documentation

### Phase 4: Testing & Tools
- [ ] Create dry-run mode for config validation
- [ ] Build provider benchmarking tool
- [ ] Add provider comparison utilities

### Migration Strategy
1. Implement new LLM abstraction alongside existing code
2. Update RiotSocialListenerAgent to use LLMProvider interface
3. Test thoroughly with Perplexity to ensure no regression
4. Add new providers incrementally
5. Update documentation and examples

## 5. Testing Strategy

### Unit Tests
- Test provider registry registration and retrieval
- Test configuration loading with various priority scenarios
- Test each adapter's response normalization
- Test error handling for missing API keys

### Integration Tests
- End-to-end test with each provider
- Configuration override testing (YAML → ENV → CLI)
- Provider switching via configuration
- Response format consistency across providers

### Validation
- Run existing Riot Pulse reports with new abstraction
- Compare output with current implementation
- Benchmark response quality across providers
- Measure performance impact

## 6. Success Criteria

- [ ] Can switch LLM providers via config.yaml without code changes
- [ ] All existing functionality works with new abstraction
- [ ] Clear error messages for misconfiguration
- [ ] At least 4 providers supported (Perplexity, OpenAI, Anthropic, xAI)
- [ ] Response format is consistent across all providers
- [ ] No performance degradation vs current implementation
- [ ] Dry-run mode successfully validates configuration

## 7. Timeline & Milestones

- **Day 1:** Core infrastructure and base interfaces
- **Day 2:** Provider adapters and configuration system
- **Day 3:** Integration and testing
- **Day 4:** Documentation and tools
- **Completion:** 4 days from approval

## 8. Open Questions

- [ ] Should we support provider-specific options in queries (e.g., temperature)?
- [ ] Do we need a provider feature matrix documentation?
- [ ] Should config.yaml be checked into git or use config.yaml.example?

## 9. References

- [Agno Framework Documentation](https://github.com/agno-ai/agno)
- [Current Perplexity Integration](../riot_pulse/agents/social_listener.py)
- [LLM Provider Comparison](https://artificialanalysis.ai/)