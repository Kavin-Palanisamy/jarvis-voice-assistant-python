"""
logger.py
Handles structured logging for the JARVIS system using loguru.
"""

import sys
from pathlib import Path
from loguru import logger

# Ensure logs directory exists
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Remove default handler
logger.remove()

# Add console handler
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{module}</cyan> | <level>{message}</level>",
    level="DEBUG",
    colorize=True
)

# Add file handler for general logs
logger.add(
    LOG_DIR / "jarvis_{time:YYYY-MM-DD}.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {module} | {message}",
    level="INFO",
    rotation="00:00",  # New file every day at midnight
    retention="7 days", # Keep logs for 7 days
    encoding="utf-8"
)

# Add file handler specifically for errors
logger.add(
    LOG_DIR / "error.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {module} | {message}\n{exception}",
    level="ERROR",
    rotation="10 MB",
    retention="7 days",
    encoding="utf-8",
    backtrace=True,
    diagnose=True
)

def get_logger():
    """Returns the configured loguru logger."""
    return logger

if __name__ == "__main__":
    log = get_logger()
    log.debug("Logger initialized successfully.")
