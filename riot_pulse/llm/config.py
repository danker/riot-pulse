"""
LLM Provider Configuration Management
"""

import logging
import os
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)


class LLMConfig:
    """Manages LLM provider configuration with priority: YAML > ENV > defaults"""

    def __init__(self, config_file: str = "config.yaml"):
        """
        Initialize configuration loader

        Args:
            config_file: Path to YAML configuration file
        """
        self.config_file = config_file
        self.config = self._load_config()

    def _load_config(self) -> dict[str, Any]:
        """
        Load configuration with priority order:
        1. YAML file
        2. Environment variables
        3. Default values
        """
        config = self._get_defaults()

        # 1. Load from YAML file if it exists
        yaml_config = self._load_yaml_config()
        if yaml_config:
            config = self._merge_configs(config, yaml_config)

        # 2. Override with environment variables
        env_config = self._load_env_config()
        config = self._merge_configs(config, env_config)

        logger.debug(f"Loaded LLM configuration: {config}")
        return config

    def _get_defaults(self) -> dict[str, Any]:
        """Get default configuration"""
        return {
            "llm": {
                "provider": "perplexity",
                "perplexity": {"model": "sonar-pro"},
                "openai": {"model": "gpt-4-turbo-preview"},
                "anthropic": {"model": "claude-3-opus-20240229"},
                "xai": {"model": "grok-1"},
            }
        }

    def _load_yaml_config(self) -> dict[str, Any] | None:
        """Load configuration from YAML file"""
        config_path = Path(self.config_file)

        # Look in current directory and parent directory
        search_paths = [
            config_path,
            Path.cwd() / config_path,
            Path.cwd().parent / config_path,
        ]

        for path in search_paths:
            if path.exists():
                logger.info(f"Loading configuration from: {path}")
                try:
                    with open(path) as f:
                        return yaml.safe_load(f) or {}
                except Exception as e:
                    logger.error(f"Error loading config file {path}: {e}")
                    return None

        logger.debug(f"No configuration file found at: {self.config_file}")
        return None

    def _load_env_config(self) -> dict[str, Any]:
        """Load configuration from environment variables"""
        config = {}

        # Check for LLM_PROVIDER environment variable
        if os.getenv("LLM_PROVIDER"):
            config["llm"] = {"provider": os.getenv("LLM_PROVIDER")}
            logger.debug(
                f"LLM provider set from environment: {config['llm']['provider']}"
            )

        # Check for model override
        if os.getenv("LLM_MODEL"):
            if "llm" not in config:
                config["llm"] = {}
            provider = config.get("llm", {}).get("provider", "perplexity")
            config["llm"][provider] = {"model": os.getenv("LLM_MODEL")}
            logger.debug(f"LLM model set from environment: {os.getenv('LLM_MODEL')}")

        return config

    def _merge_configs(
        self, base: dict[str, Any], override: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Recursively merge configuration dictionaries

        Args:
            base: Base configuration
            override: Configuration to override with

        Returns:
            Merged configuration
        """
        result = base.copy()

        for key, value in override.items():
            if (
                key in result
                and isinstance(result[key], dict)
                and isinstance(value, dict)
            ):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value

        return result

    def get_provider_config(self) -> dict[str, Any]:
        """
        Get the active provider configuration including API keys

        Returns:
            Dictionary with 'name' and 'config' keys
        """
        # Get provider name
        provider_name = self.config.get("llm", {}).get("provider", "perplexity")

        # Get provider-specific config
        provider_config = self.config.get("llm", {}).get(provider_name, {}).copy()

        # Load API key from environment
        api_key = self._get_api_key(provider_name)
        if api_key:
            provider_config["api_key"] = api_key

        return {"name": provider_name, "config": provider_config}

    def _get_api_key(self, provider: str) -> str | None:
        """
        Get API key for a provider from environment variables

        Args:
            provider: Provider name

        Returns:
            API key or None
        """
        # Map provider names to environment variable names
        env_var_map = {
            "perplexity": "PERPLEXITY_API_KEY",
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY",
            "xai": "XAI_API_KEY",
        }

        env_var = env_var_map.get(provider.lower())
        if env_var:
            api_key = os.getenv(env_var)
            if api_key:
                logger.debug(f"Loaded API key from {env_var}")
            else:
                logger.warning(f"No API key found in {env_var}")
            return api_key

        return None
