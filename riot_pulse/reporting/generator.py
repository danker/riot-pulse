"""
Report generation engine
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
import glob

from ..config import ReportConfig, RiotGames, AnalysisAspects
from ..agents.social_listener import RiotSocialListenerAgent
from ..utils.sources import inspect_response
from .formatters import MarkdownFormatter


class ReportGenerator:
    """Generates comprehensive reports based on configuration"""
    
    def __init__(self, config: ReportConfig, logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.agent = RiotSocialListenerAgent()
        self.formatter = MarkdownFormatter()
    
    def generate_report(self) -> str:
        """
        Generate a complete report based on configuration
        
        Returns:
            Path to generated report file
        """
        self.logger.info("Starting report generation...")
        self.logger.info(f"Games: {[g.value for g in self.config.games]}")
        self.logger.info(f"Aspects: {[a.value for a in self.config.aspects]}")
        
        # Collect all analysis results
        results = {}
        
        for game in self.config.games:
            game_results = {}
            game_name = RiotGames.get_display_name(game)
            
            self.logger.info(f"Analyzing {game_name}...")
            
            for aspect in self.config.aspects:
                aspect_name = AnalysisAspects.get_display_name(aspect)
                self.logger.info(f"  - {aspect_name}...")
                
                try:
                    response = self.agent.analyze_game_aspect(game, aspect, self.config.timeframe)
                    content = inspect_response(response, f"{game_name} {aspect_name}", self.logger)
                    game_results[aspect] = content
                    
                except Exception as e:
                    self.logger.error(f"Error analyzing {game_name} {aspect_name}: {e}", exc_info=True)
                    game_results[aspect] = f"Error: Unable to analyze {aspect_name} - {str(e)}"
            
            results[game] = game_results
        
        # Generate filename and create report
        filename = self._generate_filename()
        self.formatter.create_report(results, filename, self.config)
        
        self.logger.info(f"Report generated: {filename}")
        return filename
    
    def _generate_filename(self) -> str:
        """Generate filename based on current date and run number"""
        Path("reports").mkdir(exist_ok=True)
        
        now = datetime.now()
        date_str = f"{now.month}.{now.day}.{now.year}"
        
        # Get next run number for this date
        pattern = f"reports/riot-pulse-report-{date_str}.*.md"
        existing_files = glob.glob(pattern)
        
        if not existing_files:
            run_number = 1
        else:
            # Extract run numbers from existing files
            run_numbers = []
            for file in existing_files:
                try:
                    run_num = int(file.split('.')[-2])
                    run_numbers.append(run_num)
                except (ValueError, IndexError):
                    continue
            
            run_number = max(run_numbers) + 1 if run_numbers else 1
        
        return f"reports/riot-pulse-report-{date_str}.{run_number}.md"