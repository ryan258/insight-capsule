"""Centralized logging configuration for Insight Capsule."""

import logging
import sys
from pathlib import Path
from datetime import datetime
from config.settings import DATA_DIR

# Create logs directory if it doesn't exist
LOG_DIR = DATA_DIR / "logs" / "system"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Log file path with timestamp
LOG_FILE = LOG_DIR / f"insight_capsule_{datetime.now().strftime('%Y%m%d')}.log"


def setup_logger(name: str = "insight_capsule", level: int = logging.INFO) -> logging.Logger:
    """
    Set up and return a configured logger.

    Args:
        name: Logger name
        level: Logging level (default: INFO)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    # Avoid adding duplicate handlers
    if logger.hasHandlers():
        return logger

    logger.setLevel(level)

    # Console handler - simplified output for user-facing messages
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter("%(levelname)s: %(message)s")
    console_handler.setFormatter(console_format)

    # File handler - detailed output for debugging
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(file_format)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# Create default logger instance
default_logger = setup_logger()
