"""
Console Formatter module for the Reddit Fetcher application.

This module provides formatting and display utilities for console output.
"""

import datetime
from typing import List

from core.data_models import RedditPost
from utils.logger import get_logger

logger = get_logger(__name__)

class ConsoleFormatter:
    """Formats and displays Reddit posts in the console."""
    
    def format_post(self, post: RedditPost, index: int = None) -> str:
        """
        Format a Reddit post for console display.
        
        Args:
            post: The post to format
            index: Optional index for numbered lists
            
        Returns:
            str: Formatted post string
        """
        # Format the creation date
        created_date = datetime.datetime.fromtimestamp(post.created_utc)
        date_str = created_date.strftime("%Y-%m-%d %H:%M:%S")
        
        # Format the post title with optional index
        if index is not None:
            title_line = f"{index}. {post.title}"
        else:
            title_line = post.title
            
        # Build the formatted string
        lines = [
            f"\033[1m{title_line}\033[0m",  # Bold title
            f"Author: u/{post.author}",
            f"Upvotes: {post.upvotes} | Comments: {post.num_comments}",
            f"Posted: {date_str}",
            f"URL: {post.url}"
        ]
        
        # Add post content for self posts (truncated if too long)
        if post.is_self and post.selftext:
            text = post.selftext.strip()
            if len(text) > 200:
                text = text[:197] + "..."
            if text:
                lines.append(f"\nContent: {text}")
                
        return "\n".join(lines)
    
    def display_posts(self, posts: List[RedditPost]) -> None:
        """
        Display a list of Reddit posts in the console.
        
        Args:
            posts: List of posts to display
        """
        if not posts:
            print("No posts found.")
            return
            
        logger.info(f"Displaying {len(posts)} posts")
        
        for i, post in enumerate(posts, 1):
            formatted_post = self.format_post(post, i)
            
            # Print with separator except for the first post
            if i > 1:
                print("\n" + "-" * 80 + "\n")
                
            print(formatted_post)
        
        print("\n" + "=" * 80)
        print(f"Retrieved {len(posts)} posts from Reddit")
