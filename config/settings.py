"""
Settings module for the Reddit Fetcher application.

This module handles application configuration and settings management.
"""

import os
from typing import Optional
from utils.logger import configure_logger

class Settings:
    """Application settings class."""
    
    # Default settings
    DEFAULT_SUBREDDIT = "python"
    DEFAULT_POST_LIMIT = 5
    
    def __init__(self):
        """Initialize settings with default values."""
        self.subreddit = os.environ.get("REDDIT_SUBREDDIT", self.DEFAULT_SUBREDDIT)
        self.post_limit = int(os.environ.get("REDDIT_POST_LIMIT", self.DEFAULT_POST_LIMIT))
        self.verbose = False
        
        # API Settings
        self.client_id = os.environ.get("REDDIT_CLIENT_ID")
        self.client_secret = os.environ.get("REDDIT_CLIENT_SECRET")
        self.user_agent = os.environ.get("REDDIT_USER_AGENT", 
                                         "python:reddit-fetcher:v1.0 (by /u/your_username)")
        
    def configure(self, subreddit: Optional[str] = None, 
                  post_limit: Optional[int] = None,
                  verbose: bool = False) -> None:
        """
        Configure application settings.
        
        Args:
            subreddit: Subreddit name to fetch posts from
            post_limit: Number of posts to fetch
            verbose: Enable verbose logging
        """
        if subreddit:
            self.subreddit = subreddit
            
        if post_limit:
            self.post_limit = post_limit
            
        self.verbose = verbose
        
        # Configure logger based on verbosity
        configure_logger(verbose)
        
    def validate(self) -> bool:
        """
        Validate that required settings are present.
        
        Returns:
            bool: True if all required settings are present
        
        Raises:
            ValueError: If any required settings are missing
        """
        if not self.client_id:
            raise ValueError("REDDIT_CLIENT_ID is required")
        
        if not self.client_secret:
            raise ValueError("REDDIT_CLIENT_SECRET is required")
            
        if not self.subreddit:
            raise ValueError("Subreddit name is required")
            
        return True
