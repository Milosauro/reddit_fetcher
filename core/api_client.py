"""
API Client module for the Reddit Fetcher application.

This module provides the low-level Reddit API client implementation.
"""

import time
from typing import Any, Dict, List, Optional

import praw
from praw.models import Submission

from utils.logger import get_logger
from utils.error_handler import RedditAPIError, RateLimitError

logger = get_logger(__name__)

class RedditClient:
    """Low-level Reddit API client with rate limiting and error handling."""
    
    # Constants for rate limiting
    MAX_RETRIES = 3
    RETRY_DELAY = 5  # seconds
    
    def __init__(self, reddit_instance: praw.Reddit):
        """
        Initialize the Reddit client.
        
        Args:
            reddit_instance: Authenticated Reddit instance
        """
        self.reddit = reddit_instance
        
    def get_subreddit(self, subreddit_name: str):
        """
        Get a subreddit by name.
        
        Args:
            subreddit_name: Name of the subreddit
            
        Returns:
            praw.models.Subreddit: Subreddit instance
            
        Raises:
            RedditAPIError: If the subreddit cannot be retrieved
        """
        try:
            logger.debug(f"Getting subreddit: {subreddit_name}")
            return self.reddit.subreddit(subreddit_name)
        except Exception as e:
            logger.error(f"Failed to get subreddit {subreddit_name}: {str(e)}")
            raise RedditAPIError(f"Failed to get subreddit {subreddit_name}: {str(e)}")
    
    def get_latest_posts(self, subreddit_name: str, limit: int = 5) -> List[Submission]:
        """
        Get the latest posts from a subreddit.
        
        Args:
            subreddit_name: Name of the subreddit
            limit: Maximum number of posts to retrieve
            
        Returns:
            List[praw.models.Submission]: List of submission objects
            
        Raises:
            RedditAPIError: If the posts cannot be retrieved
            RateLimitError: If rate limit is hit
        """
        retries = 0
        while retries < self.MAX_RETRIES:
            try:
                logger.info(f"Fetching {limit} latest posts from r/{subreddit_name}")
                subreddit = self.get_subreddit(subreddit_name)
                
                # Get the latest posts sorted by new
                posts = list(subreddit.new(limit=limit))
                
                logger.info(f"Successfully retrieved {len(posts)} posts")
                return posts
                
            except praw.exceptions.RedditAPIException as e:
                logger.warning(f"Reddit API exception: {str(e)}")
                
                # Check if it's a rate limit error
                if any(error.error_type == "RATELIMIT" for error in e.items):
                    retries += 1
                    if retries >= self.MAX_RETRIES:
                        logger.error(f"Rate limit exceeded after {retries} retries")
                        raise RateLimitError(f"Reddit API rate limit exceeded: {str(e)}")
                    
                    # Wait before retrying
                    wait_time = self.RETRY_DELAY * retries
                    logger.info(f"Rate limit hit, waiting {wait_time} seconds before retry {retries}/{self.MAX_RETRIES}")
                    time.sleep(wait_time)
                else:
                    # For other Reddit API exceptions, raise immediately
                    raise RedditAPIError(f"Reddit API error: {str(e)}")
                    
            except Exception as e:
                logger.error(f"Failed to fetch posts: {str(e)}")
                
                # Check if it's a rate limit error (for other exception types)
                if "rate limit" in str(e).lower() or "ratelimit" in str(e).lower():
                    retries += 1
                    if retries >= self.MAX_RETRIES:
                        logger.error(f"Rate limit exceeded after {retries} retries")
                        raise RateLimitError(f"Reddit API rate limit exceeded: {str(e)}")
                    
                    # Wait before retrying
                    wait_time = self.RETRY_DELAY * retries
                    logger.info(f"Rate limit hit, waiting {wait_time} seconds before retry {retries}/{self.MAX_RETRIES}")
                    time.sleep(wait_time)
                else:
                    raise RedditAPIError(f"Failed to fetch posts from r/{subreddit_name}: {str(e)}")
                
        # This should not be reached, but just in case
        raise RedditAPIError(f"Failed to fetch posts after {self.MAX_RETRIES} retries")
