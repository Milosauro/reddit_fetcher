"""
Post Service module for the Reddit Fetcher application.

This module provides post processing services for Reddit posts.
"""

from typing import List, Callable, Optional

from core.data_models import RedditPost
from utils.logger import get_logger

logger = get_logger(__name__)

class PostService:
    """Service for processing and filtering Reddit posts."""
    
    def __init__(self):
        """Initialize the post service."""
        pass
        
    def filter_posts(self, posts: List[RedditPost], 
                    filter_func: Callable[[RedditPost], bool]) -> List[RedditPost]:
        """
        Filter posts based on a filter function.
        
        Args:
            posts: List of posts to filter
            filter_func: Function that takes a post and returns a boolean
            
        Returns:
            List[RedditPost]: Filtered list of posts
        """
        logger.debug(f"Filtering {len(posts)} posts")
        filtered_posts = [post for post in posts if filter_func(post)]
        logger.debug(f"Filtered to {len(filtered_posts)} posts")
        return filtered_posts
    
    def sort_posts(self, posts: List[RedditPost], 
                  key_func: Callable[[RedditPost], any], 
                  reverse: bool = False) -> List[RedditPost]:
        """
        Sort posts based on a key function.
        
        Args:
            posts: List of posts to sort
            key_func: Function that takes a post and returns a sort key
            reverse: Whether to sort in reverse order
            
        Returns:
            List[RedditPost]: Sorted list of posts
        """
        logger.debug(f"Sorting {len(posts)} posts")
        return sorted(posts, key=key_func, reverse=reverse)
    
    def search_posts(self, posts: List[RedditPost], query: str, 
                    case_sensitive: bool = False) -> List[RedditPost]:
        """
        Search posts for a query string in title or content.
        
        Args:
            posts: List of posts to search
            query: Search query
            case_sensitive: Whether to use case-sensitive search
            
        Returns:
            List[RedditPost]: List of matching posts
        """
        logger.debug(f"Searching {len(posts)} posts for '{query}'")
        
        if not case_sensitive:
            query = query.lower()
            return [
                post for post in posts 
                if query in post.title.lower() or 
                   (post.selftext and query in post.selftext.lower())
            ]
        else:
            return [
                post for post in posts 
                if query in post.title or 
                   (post.selftext and query in post.selftext)
            ]
    
    def filter_by_min_upvotes(self, posts: List[RedditPost], 
                             min_upvotes: int) -> List[RedditPost]:
        """
        Filter posts by minimum upvote count.
        
        Args:
            posts: List of posts to filter
            min_upvotes: Minimum number of upvotes
            
        Returns:
            List[RedditPost]: Filtered list of posts
        """
        return self.filter_posts(posts, lambda post: post.upvotes >= min_upvotes)
    
    def filter_by_min_comments(self, posts: List[RedditPost], 
                              min_comments: int) -> List[RedditPost]:
        """
        Filter posts by minimum comment count.
        
        Args:
            posts: List of posts to filter
            min_comments: Minimum number of comments
            
        Returns:
            List[RedditPost]: Filtered list of posts
        """
        return self.filter_posts(posts, lambda post: post.num_comments >= min_comments)
