"""
Logging configuration for the application.
"""
import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from core.config import settings


# Create logs directory if it doesn't exist
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

# Log file paths
app_log_file = logs_dir / "app.log"
access_log_file = logs_dir / "access.log"
error_log_file = logs_dir / "error.log"

# Log format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# Configure root logger
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATETIME_FORMAT))
console_handler.setLevel(logging.INFO)
root_logger.addHandler(console_handler)

# Application log file handler (rotating)
app_file_handler = RotatingFileHandler(
    app_log_file,
    maxBytes=10485760,  # 10MB
    backupCount=5,
    encoding="utf-8",
)
app_file_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATETIME_FORMAT))
app_file_handler.setLevel(logging.INFO)
root_logger.addHandler(app_file_handler)

# Error log file handler (rotating)
error_file_handler = RotatingFileHandler(
    error_log_file,
    maxBytes=10485760,  # 10MB
    backupCount=5,
    encoding="utf-8",
)
error_file_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATETIME_FORMAT))
error_file_handler.setLevel(logging.ERROR)
root_logger.addHandler(error_file_handler)

# Access log file handler (rotating)
access_logger = logging.getLogger("access")
access_file_handler = RotatingFileHandler(
    access_log_file,
    maxBytes=10485760,  # 10MB
    backupCount=5,
    encoding="utf-8",
)
access_file_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATETIME_FORMAT))
access_logger.setLevel(logging.INFO)
access_logger.addHandler(access_file_handler)
access_logger.propagate = False  # Don't propagate to root logger

# Set log level based on environment
if os.getenv("ENVIRONMENT", "development") == "development":
    root_logger.setLevel(logging.DEBUG)
    console_handler.setLevel(logging.DEBUG)
    app_file_handler.setLevel(logging.DEBUG)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the given name.
    
    Args:
        name: The name of the logger
        
    Returns:
        A logger instance
    """
    return logging.getLogger(name)