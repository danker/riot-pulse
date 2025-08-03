"""
Logging utilities for Riot Pulse
"""

import logging
from datetime import datetime
from pathlib import Path


def setup_logging(
    debug_mode: bool = False, log_prefix: str = "riot-pulse"
) -> logging.Logger:
    """
    Set up logging configuration

    Args:
        debug_mode: If True, enables debug logging to file
        log_prefix: Prefix for log filenames

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger("RiotPulse")

    # Clear any existing handlers to avoid duplicates
    logger.handlers.clear()

    logger.setLevel(logging.DEBUG if debug_mode else logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter("%(levelname)s: %(message)s")
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Always create a basic log file (not just debug mode)
    Path("logs").mkdir(exist_ok=True)
    log_filename = f"logs/{log_prefix}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.DEBUG if debug_mode else logging.INFO)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    logger.info(f"Logging to file: {log_filename}")

    if debug_mode:
        logger.info("Debug mode enabled - verbose logging active")

    return logger
