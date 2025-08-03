"""
Testing and validation tools for LLM providers
"""

import time
import logging
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass

from .providers import LLMProviderRegistry, get_llm_provider
from .base import BaseLLMProvider, LLMResponse

logger = logging.getLogger(__name__)


@dataclass
class ProviderTestResult:
    """Results from testing a provider"""
    provider_name: str
    model: str
    success: bool
    response_time: float
    response_length: int
    error: Optional[str] = None
    response_preview: Optional[str] = None


@dataclass
class BenchmarkResult:
    """Results from benchmarking multiple providers"""
    test_prompt: str
    results: List[ProviderTestResult]
    fastest_provider: str
    longest_response: str
    total_test_time: float


class LLMTester:
    """Testing and validation tools for LLM providers"""
    
    def __init__(self):
        """Initialize the LLM tester"""
        self.test_prompt = """
What is League of Legends? Provide a brief 2-sentence explanation of the game and its popularity.
""".strip()
    
    def dry_run_config(self, 
                      config_file: Optional[str] = None,
                      provider_override: Optional[str] = None,
                      model_override: Optional[str] = None) -> Dict[str, Any]:
        """
        Perform a dry run to validate configuration without making API calls
        
        Args:
            config_file: Path to config file
            provider_override: Provider override
            model_override: Model override
            
        Returns:
            Dictionary with validation results
        """
        result = {
            "success": False,
            "provider": None,
            "model": None,
            "errors": [],
            "warnings": []
        }
        
        try:
            # Test configuration loading and provider creation
            provider = get_llm_provider(
                config_file=config_file,
                provider_override=provider_override,
                model_override=model_override
            )
            
            result["success"] = True
            result["provider"] = provider.name
            result["model"] = provider.model
            
            # Validate API key is present
            if not provider.config.get("api_key"):
                result["warnings"].append(f"No API key found for {provider.name}")
            
            # Check if model is supported
            if provider.model not in provider.supported_models:
                result["errors"].append(
                    f"Model {provider.model} not in supported models: {provider.supported_models}"
                )
                result["success"] = False
            
        except Exception as e:
            result["errors"].append(str(e))
        
        return result
    
    def test_provider(self, 
                     provider_name: str,
                     model: Optional[str] = None,
                     custom_prompt: Optional[str] = None) -> ProviderTestResult:
        """
        Test a specific provider with a simple query
        
        Args:
            provider_name: Name of provider to test
            model: Specific model to test (optional)
            custom_prompt: Custom test prompt (optional)
            
        Returns:
            ProviderTestResult with test results
        """
        prompt = custom_prompt or self.test_prompt
        start_time = time.time()
        
        try:
            # Get provider
            provider = get_llm_provider(
                provider_override=provider_name,
                model_override=model
            )
            
            # Make test query
            response = provider.query(prompt)
            
            # Calculate metrics
            response_time = time.time() - start_time
            response_length = len(response.content)
            response_preview = response.content[:100] + "..." if len(response.content) > 100 else response.content
            
            return ProviderTestResult(
                provider_name=provider.name,
                model=provider.model,
                success=True,
                response_time=response_time,
                response_length=response_length,
                response_preview=response_preview
            )
            
        except Exception as e:
            response_time = time.time() - start_time
            return ProviderTestResult(
                provider_name=provider_name,
                model=model or "unknown",
                success=False,
                response_time=response_time,
                response_length=0,
                error=str(e)
            )
    
    def benchmark_providers(self, 
                           providers: Optional[List[str]] = None,
                           custom_prompt: Optional[str] = None) -> BenchmarkResult:
        """
        Benchmark multiple providers with the same prompt
        
        Args:
            providers: List of provider names to test (default: all available)
            custom_prompt: Custom test prompt (optional)
            
        Returns:
            BenchmarkResult with comparison results
        """
        if providers is None:
            providers = LLMProviderRegistry.list_providers()
        
        prompt = custom_prompt or self.test_prompt
        start_time = time.time()
        
        results = []
        
        for provider_name in providers:
            logger.info(f"Testing provider: {provider_name}")
            result = self.test_provider(provider_name, custom_prompt=prompt)
            results.append(result)
        
        total_time = time.time() - start_time
        
        # Find fastest provider (among successful ones)
        successful_results = [r for r in results if r.success]
        fastest_provider = "none"
        if successful_results:
            fastest = min(successful_results, key=lambda x: x.response_time)
            fastest_provider = fastest.provider_name
        
        # Find longest response (among successful ones)
        longest_response = "none"
        if successful_results:
            longest = max(successful_results, key=lambda x: x.response_length)
            longest_response = longest.provider_name
        
        return BenchmarkResult(
            test_prompt=prompt,
            results=results,
            fastest_provider=fastest_provider,
            longest_response=longest_response,
            total_test_time=total_time
        )
    
    def list_available_providers(self) -> Dict[str, Dict[str, Any]]:
        """
        List all available providers with their details
        
        Returns:
            Dictionary mapping provider names to their details
        """
        providers = {}
        
        for provider_name in LLMProviderRegistry.list_providers():
            try:
                provider_class = LLMProviderRegistry._providers[provider_name]
                instance = provider_class.__new__(provider_class)
                
                providers[provider_name] = {
                    "default_model": instance.default_model,
                    "supported_models": instance.supported_models,
                    "description": instance.__doc__ or "No description available"
                }
            except Exception as e:
                providers[provider_name] = {
                    "error": str(e)
                }
        
        return providers
    
    def print_dry_run_results(self, result: Dict[str, Any]) -> None:
        """Print dry run results in a user-friendly format"""
        print("🔍 Configuration Validation Results")
        print("=" * 40)
        
        if result["success"]:
            print(f"✅ Configuration valid")
            print(f"   Provider: {result['provider']}")
            print(f"   Model: {result['model']}")
        else:
            print(f"❌ Configuration invalid")
        
        if result["warnings"]:
            print("\n⚠️  Warnings:")
            for warning in result["warnings"]:
                print(f"   - {warning}")
        
        if result["errors"]:
            print("\n❌ Errors:")
            for error in result["errors"]:
                print(f"   - {error}")
    
    def print_benchmark_results(self, result: BenchmarkResult) -> None:
        """Print benchmark results in a user-friendly format"""
        print("🏆 Provider Benchmark Results")
        print("=" * 50)
        print(f"Test prompt: {result.test_prompt[:60]}...")
        print(f"Total test time: {result.total_test_time:.2f}s")
        print(f"Fastest provider: {result.fastest_provider}")
        print(f"Longest response: {result.longest_response}")
        print()
        
        for test_result in result.results:
            status = "✅" if test_result.success else "❌"
            print(f"{status} {test_result.provider_name} ({test_result.model})")
            
            if test_result.success:
                print(f"   Time: {test_result.response_time:.2f}s")
                print(f"   Length: {test_result.response_length} chars")
                print(f"   Preview: {test_result.response_preview}")
            else:
                print(f"   Error: {test_result.error}")
            print()


def main():
    """Main CLI for LLM testing tools"""
    import argparse
    
    parser = argparse.ArgumentParser(description="LLM Provider Testing Tools")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Dry run command
    dry_run_parser = subparsers.add_parser("dry-run", help="Validate configuration")
    dry_run_parser.add_argument("--config", help="Configuration file path")
    dry_run_parser.add_argument("--provider", help="Provider override")
    dry_run_parser.add_argument("--model", help="Model override")
    
    # Test command
    test_parser = subparsers.add_parser("test", help="Test a specific provider")
    test_parser.add_argument("provider", help="Provider name to test")
    test_parser.add_argument("--model", help="Specific model to test")
    test_parser.add_argument("--prompt", help="Custom test prompt")
    
    # Benchmark command
    benchmark_parser = subparsers.add_parser("benchmark", help="Benchmark all providers")
    benchmark_parser.add_argument("--providers", nargs="*", help="Specific providers to test")
    benchmark_parser.add_argument("--prompt", help="Custom test prompt")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List available providers")
    
    args = parser.parse_args()
    tester = LLMTester()
    
    if args.command == "dry-run":
        result = tester.dry_run_config(
            config_file=args.config,
            provider_override=args.provider,
            model_override=args.model
        )
        tester.print_dry_run_results(result)
    
    elif args.command == "test":
        result = tester.test_provider(
            provider_name=args.provider,
            model=args.model,
            custom_prompt=args.prompt
        )
        if result.success:
            print(f"✅ {result.provider_name} test successful!")
            print(f"   Time: {result.response_time:.2f}s")
            print(f"   Response: {result.response_preview}")
        else:
            print(f"❌ {result.provider_name} test failed: {result.error}")
    
    elif args.command == "benchmark":
        result = tester.benchmark_providers(
            providers=args.providers,
            custom_prompt=args.prompt
        )
        tester.print_benchmark_results(result)
    
    elif args.command == "list":
        providers = tester.list_available_providers()
        print("📋 Available LLM Providers")
        print("=" * 30)
        for name, details in providers.items():
            if "error" in details:
                print(f"❌ {name}: {details['error']}")
            else:
                print(f"✅ {name}")
                print(f"   Default: {details['default_model']}")
                print(f"   Models: {', '.join(details['supported_models'][:3])}...")
                print()
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()