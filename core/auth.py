"""
Authentication module for the Reddit Fetcher application.

This module handles Reddit API authentication.
"""

import praw
from config.credentials import CredentialsManager
from utils.logger import get_logger
from utils.error_handler import RedditAuthError

logger = get_logger(__name__)

class RedditAuthenticator:
    """Handles authentication with the Reddit API."""
    
    def __init__(self):
        """Initialize the Reddit authenticator."""
        self.credentials_manager = CredentialsManager()
        
    def authenticate(self) -> praw.Reddit:
        """
        Authenticate with the Reddit API.
        
        Returns:
            praw.Reddit: Authenticated Reddit instance
            
        Raises:
            RedditAuthError: If authentication fails
        """
        try:
            logger.info("Authenticating with Reddit API")
            credentials = self.credentials_manager.get_credentials()
            
            reddit = praw.Reddit(
                client_id=credentials['client_id'],
                client_secret=credentials['client_secret'],
                user_agent=credentials['user_agent']
            )
            
            # Verify credentials by making a simple API call
            # This will raise an exception if authentication fails
            reddit.user.me()
            
            logger.info("Authentication successful")
            return reddit
            
        except Exception as e:
            logger.error(f"Authentication failed: {str(e)}")
            raise RedditAuthError(f"Failed to authenticate with Reddit API: {str(e)}")
