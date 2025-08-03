from agno.agent import Agent
from agno.models.perplexity import Perplexity
import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
import glob
import logging
from pprint import pformat

# Load environment variables from .env file
load_dotenv()

class RiotResearchAgent(Agent):
    def __init__(self, perplexity_api_key: str = None):
        # Get API key from environment variable if not provided
        if perplexity_api_key is None:
            perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")
            if not perplexity_api_key:
                raise ValueError("PERPLEXITY_API_KEY environment variable is required")
        
        # Initialize the agent with Perplexity model
        super().__init__(
            name="Riot Games Social Listening Agent",
            model=Perplexity(id="sonar-pro", api_key=perplexity_api_key),
            description="Monitors community sentiment and trends across all Riot Games titles",
            instructions=[
                "You are a gaming industry analyst specializing in Riot Games",
                "Focus on community sentiment, competitive meta, and player feedback",
                "Always provide specific sources and actionable insights",
                "Monitor: VALORANT, League of Legends, 2XKO, Teamfight Tactics, Riftbound",
                "Structure responses with clear sections: Summary, Key Themes, Sentiment, Sources"
            ],
            markdown=True
        )
        # Add tools to the agent
        self.add_tool(self.research_game_sentiment)
        self.add_tool(self.monitor_patch_reactions)
        self.add_tool(self.track_competitive_meta)
        self.add_tool(self.crisis_detection)
        self.add_tool(self.trending_analysis)

    def research_game_sentiment(self, game: str, timeframe: str = "24 hours") -> str:
        """
        Research current community sentiment for a specific Riot game
        
        Args:
            game: The Riot game to research (VALORANT, League of Legends, 2XKO, etc.)
            timeframe: How far back to look (24 hours, 1 week, etc.)
        
        Returns:
            Detailed sentiment analysis with sources
        """
        
        query = f"""What are players saying about {game} in the past {timeframe}? 
        Focus on Reddit, Twitter, and gaming forums. 
        Highlight any trending topics, complaints, praise, or major discussions.
        Include sentiment analysis and specific examples."""
        
        return f"Researching {game} sentiment for {timeframe}: {query}"

    def monitor_patch_reactions(self, game: str, patch_version: str = None) -> str:
        """
        Analyze community reaction to recent game patches
        
        Args:
            game: The Riot game to analyze
            patch_version: Specific patch version (optional)
        
        Returns:
            Patch reaction analysis with community sentiment
        """
        
        patch_info = f" patch {patch_version}" if patch_version else " latest patch"
        
        query = f"""Analyze community reaction to the{patch_info} for {game}.
        Look for:
        1. Balance complaints or praise
        2. Meta shifts discussions  
        3. Pro player opinions
        4. Reddit sentiment trends
        5. Overall community satisfaction
        
        Include specific examples and sentiment scoring."""
        
        return f"Analyzing {game}{patch_info} reactions: {query}"

    def track_competitive_meta(self, game: str) -> str:
        """
        Research current competitive meta and tier discussions
        
        Args:
            game: The Riot game to analyze
        
        Returns:
            Current meta analysis and competitive trends
        """
        
        query = f"""What's the current competitive meta discussion for {game}?
        Focus on:
        - Character/agent tier lists and rankings
        - Pro tournament picks and bans
        - Strategy discussions and guides
        - Community debates about balance
        - Recent tournament results and impact
        
        Provide current meta snapshot with sources."""
        
        return f"Tracking {game} competitive meta: {query}"

    def crisis_detection(self, keyword: str = None) -> str:
        """
        Monitor for potential PR issues, controversies, or negative sentiment spikes
        
        Args:
            keyword: Specific topic to monitor (optional)
        
        Returns:
            Crisis monitoring report with severity assessment
        """
        
        if keyword:
            query = f"""Search for any controversies, complaints, or negative sentiment 
            around {keyword} in Riot Games communities in the past 48 hours."""
        else:
            query = """Monitor for any major controversies, complaints, or negative sentiment 
            spikes across all Riot Games in the past 48 hours."""
            
        query += """
        Look for:
        - Reddit drama threads
        - Twitter complaints and backlash
        - Streamer criticisms
        - Community boycotts or protests
        - Viral negative content
        
        Rate the severity (Low/Medium/High) and provide context."""
        
        return f"Crisis monitoring{' for ' + keyword if keyword else ''}: {query}"

    def trending_analysis(self) -> str:
        """
        Identify trending topics and viral content across all Riot games
        
        Returns:
            Trending topics report ranked by engagement
        """
        
        query = """What are the top trending topics in Riot Games communities today?
        Check Reddit, Twitter, gaming news sites, and forums for:
        - Viral clips, plays, or moments
        - New announcement reactions
        - Community memes and discussions  
        - Esports highlights and drama
        - Content creator highlights
        
        Rank by engagement level and buzz intensity."""
        
        return f"Analyzing trending topics: {query}"

def get_next_run_number(date_str: str) -> int:
    """
    Get the next run number for a given date
    
    Args:
        date_str: Date string in format M.D.YYYY
    
    Returns:
        Next run number for that date
    """
    # Look for existing files with this date pattern in reports folder
    pattern = f"reports/riot-social-listening-report-{date_str}.*.md"
    existing_files = glob.glob(pattern)
    
    if not existing_files:
        return 1
    
    # Extract run numbers from existing files
    run_numbers = []
    for file in existing_files:
        try:
            # Extract the run number from filename
            run_num = int(file.split('.')[-2])
            run_numbers.append(run_num)
        except (ValueError, IndexError):
            continue
    
    return max(run_numbers) + 1 if run_numbers else 1

def generate_filename() -> str:
    """
    Generate filename based on current date and run number
    Format: reports/riot-social-listening-report-M.D.YYYY.N.md
    """
    # Ensure reports directory exists
    Path("reports").mkdir(exist_ok=True)
    
    now = datetime.now()
    date_str = f"{now.month}.{now.day}.{now.year}"
    run_number = get_next_run_number(date_str)
    
    return f"reports/riot-social-listening-report-{date_str}.{run_number}.md"

def create_markdown_report(results: dict, filename: str) -> None:
    """
    Create a markdown report from agent results
    
    Args:
        results: Dictionary containing agent outputs
        filename: Output filename
    """
    now = datetime.now()
    timestamp = now.strftime("%B %d, %Y at %I:%M %p")
    
    # Process each result to handle formatting
    processed_results = {}
    for key, content in results.items():
        # Replace escaped newlines with actual newlines
        if isinstance(content, str):
            # Handle escaped newlines
            content = content.replace('\\n', '\n')
            # Ensure proper markdown formatting
            content = content.strip()
        processed_results[key] = content
    
    markdown_content = f"""# Riot Games Social Listening Report

**Date:** {timestamp}  
**Report:** {filename}

---

## Executive Summary

This report provides an automated analysis of community sentiment, trending topics, and potential issues across Riot Games titles including VALORANT, League of Legends, 2XKO, Teamfight Tactics, and Riftbound.

---

## VALORANT Community Sentiment

{processed_results.get('valorant_sentiment', 'No data available')}

---

## League of Legends Patch Analysis

{processed_results.get('league_patch', 'No data available')}

---

## Crisis Monitoring Report

{processed_results.get('crisis_report', 'No data available')}

---

## Trending Topics Across All Games

{processed_results.get('trending', 'No data available')}

---

*Report generated by Riot Games Social Listening Agent using Perplexity AI*
"""
    
    # Write to file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

def setup_logging(debug_mode: bool = False) -> logging.Logger:
    """
    Set up logging configuration
    
    Args:
        debug_mode: If True, enables debug logging to file
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger('RiotSocialListener')
    logger.setLevel(logging.DEBUG if debug_mode else logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # Always create a basic log file (not just debug mode)
    Path("logs").mkdir(exist_ok=True)
    log_filename = f"logs/riot-social-{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.DEBUG if debug_mode else logging.INFO)
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    logger.info(f"Logging to file: {log_filename}")
    
    if debug_mode:
        logger.info("Debug mode enabled - verbose logging active")
    
    return logger

def extract_sources_from_content(content: str) -> tuple[str, list[str]]:
    """
    Extract source URLs from Perplexity response content
    
    Args:
        content: The response content that may contain sources
    
    Returns:
        Tuple of (cleaned_content, list_of_source_urls)
    """
    import re
    
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

def inspect_response(response, task_name: str, logger: logging.Logger) -> str:
    """
    Inspect and log response structure, then extract content with proper source formatting
    
    Args:
        response: The response object from agent.run()
        task_name: Name of the task for logging
        logger: Logger instance
    
    Returns:
        Extracted content string with proper source references
    """
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

# Usage example
def main(debug_mode: bool = False):
    # Set up logging
    logger = setup_logging(debug_mode)
    
    # Initialize the Agno agent (API key from environment)
    agent = RiotResearchAgent()
    
    # Generate filename for this run
    filename = generate_filename()
    
    print("🎮 Starting Riot Games Social Listening Agent...")
    print(f"📝 Report will be saved to: {filename}")
    if debug_mode:
        print("🐛 Debug mode enabled - detailed logs will be saved")
    
    # Dictionary to store results
    results = {}
    
    # Daily sentiment check
    print("🔍 Analyzing VALORANT sentiment...")
    try:
        response = agent.run("Check VALORANT community sentiment for the past 24 hours")
        results['valorant_sentiment'] = inspect_response(response, "VALORANT Sentiment", logger)
    except Exception as e:
        logger.error(f"Error analyzing VALORANT sentiment: {e}", exc_info=True)
        print(f"⚠️  Error analyzing VALORANT sentiment: {e}")
        results['valorant_sentiment'] = f"Error: Unable to analyze VALORANT sentiment - {str(e)}"
    
    # Patch analysis
    print("🔍 Analyzing League of Legends patch reactions...")
    try:
        response = agent.run("Analyze reactions to the latest League of Legends patch")
        results['league_patch'] = inspect_response(response, "League Patch Analysis", logger)
    except Exception as e:
        logger.error(f"Error analyzing League patch: {e}", exc_info=True)
        print(f"⚠️  Error analyzing League patch: {e}")
        results['league_patch'] = f"Error: Unable to analyze League patch reactions - {str(e)}"
    
    # Crisis monitoring  
    print("🔍 Monitoring for potential issues...")
    try:
        response = agent.run("Check for any brewing controversies or negative sentiment spikes")
        results['crisis_report'] = inspect_response(response, "Crisis Monitoring", logger)
    except Exception as e:
        logger.error(f"Error in crisis monitoring: {e}", exc_info=True)
        print(f"⚠️  Error in crisis monitoring: {e}")
        results['crisis_report'] = f"Error: Unable to monitor for issues - {str(e)}"
    
    # Trending topics
    print("🔍 Identifying trending topics...")
    try:
        response = agent.run("What's trending across all Riot games today?")
        results['trending'] = inspect_response(response, "Trending Topics", logger)
    except Exception as e:
        logger.error(f"Error identifying trends: {e}", exc_info=True)
        print(f"⚠️  Error identifying trends: {e}")
        results['trending'] = f"Error: Unable to identify trending topics - {str(e)}"
    
    # Create the markdown report
    create_markdown_report(results, filename)
    print(f"✅ Report successfully generated: {filename}")

if __name__ == "__main__":
    import sys
    
    # Check for debug flag
    debug_mode = "--debug" in sys.argv or "-d" in sys.argv
    
    try:
        main(debug_mode=debug_mode)
    except KeyboardInterrupt:
        print("\n👋 Agent stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")