"""
Command line interface for Riot Pulse
"""

import argparse
import sys
from typing import List

from .config import ReportConfig, RiotGames, AnalysisAspects
from .reporting.generator import ReportGenerator
from .utils.logging import setup_logging


def parse_games(games_str: List[str]) -> List[str]:
    """Parse and validate game arguments"""
    if not games_str:
        return ["valorant", "league_of_legends"]  # Default games
    
    # Handle comma-separated games in a single argument
    games = []
    for game_str in games_str:
        games.extend([g.strip() for g in game_str.split(',')])
    
    return games


def parse_aspects(aspects_str: List[str]) -> List[str]:
    """Parse and validate aspect arguments"""
    if not aspects_str:
        return ["sentiment", "patches", "crisis"]  # Default aspects
    
    # Handle comma-separated aspects in a single argument
    aspects = []
    for aspect_str in aspects_str:
        aspects.extend([a.strip() for a in aspect_str.split(',')])
    
    return aspects


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Riot Pulse - AI-powered social listening for Riot Games communities",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m riot_pulse --games valorant,league --aspects sentiment,patches
  python -m riot_pulse --games all --aspects all --timeframe "1 week"
  python -m riot_pulse --games valorant --aspects crisis --debug

Available games: valorant, league_of_legends, teamfight_tactics, legends_of_runeterra, riot_forge, all
Available aspects: sentiment, patches, esports, crisis, trending, meta, all
        """
    )
    
    parser.add_argument(
        '--games', '-g',
        nargs='*',
        default=None,
        help='Games to analyze (comma-separated or space-separated). Use "all" for all games.'
    )
    
    parser.add_argument(
        '--aspects', '-a', 
        nargs='*',
        default=None,
        help='Analysis aspects to perform (comma-separated or space-separated). Use "all" for all aspects.'
    )
    
    parser.add_argument(
        '--timeframe', '-t',
        default="24 hours",
        help='Time period to analyze (default: "24 hours")'
    )
    
    parser.add_argument(
        '--debug', '-d',
        action='store_true',
        help='Enable debug logging'
    )
    
    parser.add_argument(
        '--list-games',
        action='store_true',
        help='List available games and exit'
    )
    
    parser.add_argument(
        '--list-aspects',
        action='store_true',
        help='List available analysis aspects and exit'
    )
    
    args = parser.parse_args()
    
    # Handle list commands
    if args.list_games:
        print("Available games:")
        for game in RiotGames:
            print(f"  {game.value}: {RiotGames.get_display_name(game)}")
        return
    
    if args.list_aspects:
        print("Available analysis aspects:")
        for aspect in AnalysisAspects:
            print(f"  {aspect.value}: {AnalysisAspects.get_display_name(aspect)}")
        return
    
    # Parse arguments
    games = parse_games(args.games)
    aspects = parse_aspects(args.aspects)
    
    try:
        # Create configuration
        config = ReportConfig.from_cli_args(
            games=games,
            aspects=aspects,
            timeframe=args.timeframe,
            debug_mode=args.debug
        )
        
        # Set up logging
        logger = setup_logging(debug_mode=args.debug, log_prefix="riot-pulse")
        
        # Generate report
        generator = ReportGenerator(config, logger)
        filename = generator.generate_report()
        
        print(f"✅ Report generated successfully: {filename}")
        
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        parser.print_help()
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Analysis stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()