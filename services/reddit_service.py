"""
Reddit Service module for the Reddit Fetcher application.

This module provides high-level services for interacting with the Reddit API.
"""

from typing import List

import praw

from core.api_client import RedditClient
from core.data_models import RedditPost
from utils.logger import get_logger

logger = get_logger(__name__)

class RedditService:
    """High-level service for interacting with the Reddit API."""
    
    def __init__(self, reddit_instance: praw.Reddit):
        """
        Initialize the Reddit service.
        
        Args:
            reddit_instance: Authenticated Reddit instance
        """
        self.client = RedditClient(reddit_instance)
        
    def get_latest_posts(self, subreddit_name: str, limit: int = 5) -> List[RedditPost]:
        """
        Get the latest posts from a subreddit.
        
        Args:
            subreddit_name: Name of the subreddit
            limit: Maximum number of posts to retrieve
            
        Returns:
            List[RedditPost]: List of post data models
        """
        logger.info(f"Getting latest {limit} posts from r/{subreddit_name}")
        
        # Get raw submissions from API client
        raw_posts = self.client.get_latest_posts(subreddit_name, limit)
        
        # Convert to our data model
        posts = [RedditPost.from_praw_submission(post) for post in raw_posts]
        
        logger.info(f"Retrieved and processed {len(posts)} posts")
        return posts
    
    def get_top_posts(self, subreddit_name: str, limit: int = 5, time_filter: str = "day") -> List[RedditPost]:
        """
        Get the top posts from a subreddit.
        
        Args:
            subreddit_name: Name of the subreddit
            limit: Maximum number of posts to retrieve
            time_filter: Time filter (hour, day, week, month, year, all)
            
        Returns:
            List[RedditPost]: List of post data models
        """
        logger.info(f"Getting top {limit} posts from r/{subreddit_name} for time period: {time_filter}")
        
        try:
            subreddit = self.client.get_subreddit(subreddit_name)
            raw_posts = list(subreddit.top(time_filter=time_filter, limit=limit))
            
            # Convert to our data model
            posts = [RedditPost.from_praw_submission(post) for post in raw_posts]
            
            logger.info(f"Retrieved and processed {len(posts)} posts")
            return posts
            
        except Exception as e:
            logger.error(f"Error getting top posts: {str(e)}")
            raise
