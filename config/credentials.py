"""
Credentials module for the Reddit Fetcher application.

This module handles API credentials management.
"""

import os
from typing import Dict
from dotenv import load_dotenv
from pathlib import Path
from utils.logger import get_logger

logger = get_logger(__name__)

class CredentialsManager:
    """Manages API credentials for Reddit authentication."""
    def __init__(self):
        """Initialize the credentials manager."""
        self._credentials = {}
        
    def load_from_env(self) -> Dict[str, str]:
        """
        Load credentials from environment variables.
        
        Returns:
            Dict[str, str]: Dictionary containing credentials
            
        Raises:
            ValueError: If required credentials are missing
        """
        # Load variables from .env file
        dotenv_path = Path(__file__).parent.parent / '.env'
        load_dotenv(dotenv_path)
        logger.debug(f"Attempting to load .env file from: {dotenv_path}")
        
        credentials = {
            'client_id': os.environ.get('REDDIT_CLIENT_ID'),
            'client_secret': os.environ.get('REDDIT_CLIENT_SECRET'),
            'user_agent': os.environ.get('REDDIT_USER_AGENT')
        }
        
        # Validate required credentials
        if not credentials['client_id'] or not credentials['client_secret']:
            logger.error("Missing required Reddit API credentials")
            raise ValueError(
                "Reddit API credentials are required. "
                "Please set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET environment variables."
            )
            
        if not credentials['user_agent']:
            # Set default user agent if not provided
            credentials['user_agent'] = f"python:reddit-fetcher:v1.0 (by /u/your_username)"
            logger.warning(f"User agent not specified, using default: {credentials['user_agent']}")
            
        self._credentials = credentials
        logger.debug("Credentials loaded successfully")
        return credentials
        
    def get_credentials(self) -> Dict[str, str]:
        """
        Get the loaded credentials.
        
        Returns:
            Dict[str, str]: Dictionary containing credentials
        """
        if not self._credentials:
            return self.load_from_env()
        return self._credentials
