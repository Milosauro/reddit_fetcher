"""
Validators module for the Reddit Fetcher application.

This module provides utilities for input validation.
"""

import re
from typing import Optional

from utils.logger import get_logger

logger = get_logger(__name__)

def validate_subreddit_name(subreddit: str) -> bool:
    """
    Validate a subreddit name.
    
    Args:
        subreddit: Name of the subreddit to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not subreddit:
        logger.error("Subreddit name cannot be empty")
        return False
        
    # Remove 'r/' prefix if present
    if subreddit.startswith('r/'):
        subreddit = subreddit[2:]
        
    # Reddit subreddit naming rules
    pattern = r'^[A-Za-z0-9]\w{2,20}$'
    
    if not re.match(pattern, subreddit):
        logger.error(f"Invalid subreddit name: {subreddit}")
        return False
        
    return True

def validate_post_limit(limit: int) -> Optional[int]:
    """
    Validate and normalize the post limit.
    
    Args:
        limit: Number of posts to retrieve
        
    Returns:
        int: Normalized limit or None if invalid
    """
    try:
        limit = int(limit)
    except (TypeError, ValueError):
        logger.error(f"Invalid post limit: {limit}")
        return None
        
    # Enforce minimum and maximum limits
    if limit < 1:
        logger.warning(f"Post limit {limit} is too low, setting to 1")
        return 1
        
    if limit > 100:
        logger.warning(f"Post limit {limit} is too high, setting to 100")
        return 100
        
    return limit
