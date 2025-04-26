"""
Error Handler module for the Reddit Fetcher application.

This module provides error handling utilities and custom exceptions.
"""

import sys
from typing import Union

from utils.logger import get_logger

logger = get_logger(__name__)

# Custom exceptions
class RedditFetcherError(Exception):
    """Base exception for Reddit Fetcher application errors."""
    pass

class RedditAuthError(RedditFetcherError):
    """Exception raised for authentication errors."""
    pass

class RedditAPIError(RedditFetcherError):
    """Exception raised for Reddit API errors."""
    pass

class RateLimitError(RedditAPIError):
    """Exception raised when the Reddit API rate limit is exceeded."""
    pass

class ConfigurationError(RedditFetcherError):
    """Exception raised for configuration errors."""
    pass


def handle_application_error(error: Exception) -> int:
    """
    Handle application errors and return an appropriate exit code.
    
    Args:
        error: The exception to handle
        
    Returns:
        int: Exit code for the application
    """
    if isinstance(error, RedditAuthError):
        logger.error(f"Authentication error: {str(error)}")
        print(f"Error: Failed to authenticate with Reddit API. Please check your credentials.")
        return 1
        
    elif isinstance(error, RateLimitError):
        logger.error(f"Rate limit error: {str(error)}")
        print(f"Error: Reddit API rate limit exceeded. Please try again later.")
        return 2
        
    elif isinstance(error, RedditAPIError):
        logger.error(f"API error: {str(error)}")
        print(f"Error: {str(error)}")
        return 3
        
    elif isinstance(error, ConfigurationError):
        logger.error(f"Configuration error: {str(error)}")
        print(f"Error: {str(error)}")
        return 4
        
    else:
        logger.error(f"Unexpected error: {str(error)}", exc_info=True)
        print(f"An unexpected error occurred: {str(error)}")
        return 99
