"""
Output Manager module for the Reddit Fetcher application.

This module provides utilities for managing different output formats.
"""

import json
from typing import List, Dict, Any

from core.data_models import RedditPost
from utils.logger import get_logger

logger = get_logger(__name__)

class OutputManager:
    """Manages different output formats for the application."""
    
    def __init__(self):
        """Initialize the output manager."""
        pass
        
    def posts_to_dict(self, posts: List[RedditPost]) -> List[Dict[str, Any]]:
        """
        Convert posts to dictionary format for JSON output.
        
        Args:
            posts: List of posts to convert
            
        Returns:
            List[Dict[str, Any]]: List of post dictionaries
        """
        return [
            {
                'id': post.id,
                'title': post.title,
                'author': post.author,
                'upvotes': post.upvotes,
                'score': post.score,
                'url': post.url,
                'created_utc': post.created_utc,
                'num_comments': post.num_comments,
                'is_self': post.is_self,
                'selftext': post.selftext if post.is_self else None
            }
            for post in posts
        ]
        
    def export_to_json(self, posts: List[RedditPost], file_path: str) -> None:
        """
        Export posts to a JSON file.
        
        Args:
            posts: List of posts to export
            file_path: Path to the output file
        """
        try:
            logger.info(f"Exporting {len(posts)} posts to JSON: {file_path}")
            
            # Convert posts to dictionary format
            posts_dict = self.posts_to_dict(posts)
            
            # Write to file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(posts_dict, f, indent=2, ensure_ascii=False)
                
            logger.info(f"Successfully exported posts to {file_path}")
            
        except Exception as e:
            logger.error(f"Failed to export posts to JSON: {str(e)}")
            raise
