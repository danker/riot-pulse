"""
Source extraction utilities for Riot Pulse
"""

import re
from typing import Tuple, List


def extract_sources_from_content(content: str) -> Tuple[str, List[str]]:
    """
    Extract source URLs from Perplexity response content
    
    Args:
        content: The response content that may contain sources
    
    Returns:
        Tuple of (cleaned_content, list_of_source_urls)
    """
    # Look for Perplexity-style source citations
    # Pattern matches [1], [2], etc. and tries to find corresponding URLs
    citation_pattern = r'\[(\d+)\]'
    citations = re.findall(citation_pattern, content)
    
    # Look for URLs in the content
    url_pattern = r'https?://[^\s\)\]]+'
    urls = re.findall(url_pattern, content)
    
    # Create proper markdown references
    cleaned_content = content
    sources = []
    
    if urls:
        # Add proper reference section
        cleaned_content += "\n\n### Sources\n"
        for i, url in enumerate(urls[:10], 1):  # Limit to 10 sources
            cleaned_content += f"[{i}] {url}\n"
            sources.append(url)
    
    return cleaned_content, sources


def inspect_response(response, task_name: str, logger) -> str:
    """
    Inspect and log response structure, then extract content with proper source formatting
    
    Args:
        response: The response object from agent.run()
        task_name: Name of the task for logging
        logger: Logger instance
    
    Returns:
        Extracted content string with proper source references
    """
    from pprint import pformat
    
    logger.debug(f"\n{'='*60}")
    logger.debug(f"Task: {task_name}")
    logger.debug(f"Response type: {type(response)}")
    logger.debug(f"Response attributes: {dir(response)}")
    
    # Try to extract content with detailed logging
    content = None
    
    # Check for 'content' attribute
    if hasattr(response, 'content'):
        content = response.content
        logger.debug(f"Found 'content' attribute")
        logger.debug(f"Content type: {type(content)}")
        logger.debug(f"Content preview (first 200 chars): {str(content)[:200]}")
    
    # Check for other common attributes
    elif hasattr(response, 'text'):
        content = response.text
        logger.debug(f"Found 'text' attribute")
    elif hasattr(response, 'message'):
        content = response.message
        logger.debug(f"Found 'message' attribute")
    elif hasattr(response, 'result'):
        content = response.result
        logger.debug(f"Found 'result' attribute")
    else:
        # Last resort - convert to string
        content = str(response)
        logger.debug(f"No standard attributes found, converting to string")
    
    # Log the full response object for debugging
    logger.debug(f"Full response object:\n{pformat(vars(response) if hasattr(response, '__dict__') else response)}")
    
    # Extract and format sources properly
    if content:
        cleaned_content, sources = extract_sources_from_content(str(content))
        logger.info(f"Extracted {len(sources)} sources for {task_name}")
        return cleaned_content
    
    return content