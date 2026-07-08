"""
SkillGap AI - Centralized Logger
Provides consistent logging across all modules.
"""

import logging
import os
from datetime import datetime


def setup_logger(name: str = "skillgap_ai", level: int = logging.INFO) -> logging.Logger:
    """
    Set up and return a configured logger instance.
    
    Args:
        name: Logger name (module identifier)
        level: Logging level (default: INFO)
    
    Returns:
        Configured Logger instance
    """
    logger = logging.getLogger(name)
    
    if logger.handlers:
        return logger
    
    logger.setLevel(level)
    
    # Console handler with colorized output
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    
    # Formatter
    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (optional - logs to file if logs/ dir exists)
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
    try:
        os.makedirs(logs_dir, exist_ok=True)
        log_file = os.path.join(logs_dir, f"skillgap_ai_{datetime.now().strftime('%Y%m%d')}.log")
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception:
        pass  # File logging is optional; don't fail if unavailable
    
    return logger


# Default application logger
logger = setup_logger("skillgap_ai")
