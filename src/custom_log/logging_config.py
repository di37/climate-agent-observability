"""Logging configuration."""

import logging
from ..config.settings import LOG_FILE

def setup_logging(level=logging.INFO):
    """
    Configure application logging to both file and console.
    
    Args:
        level: Logging level (default: INFO)
    """
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(LOG_FILE),  # Save to file
            logging.StreamHandler()  # Print to console
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured, saving to: {LOG_FILE}")
    
    return logger

