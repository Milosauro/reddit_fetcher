"""
Logger module for the Reddit Fetcher application.

This module provides logging utilities for the application.
"""

import logging
import sys
from typing import Optional

# Default logger format
DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Create logger
_logger = None

def configure_logger(verbose: bool = False) -> logging.Logger:
    """
    Configure the application logger.
    
    Args:
        verbose: Whether to enable verbose logging
        
    Returns:
        logging.Logger: Configured logger instance
    """
    global _logger
    
    if _logger:
        return _logger
        
    # Create logger
    _logger = logging.getLogger("reddit_fetcher")
    
    # Set log level based on verbosity
    level = logging.DEBUG if verbose else logging.INFO
    _logger.setLevel(level)
    
    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    
    # Create formatter
    formatter = logging.Formatter(DEFAULT_FORMAT)
    handler.setFormatter(formatter)
    
    # Add handler to logger
    _logger.addHandler(handler)
    
    return _logger

def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance.
    
    Args:
        name: Logger name (optional)
        
    Returns:
        logging.Logger: Logger instance
    """
    global _logger
    
    if not _logger:
        _logger = configure_logger()
        
    if name:
        return _logger.getChild(name)
        
    return _logger
