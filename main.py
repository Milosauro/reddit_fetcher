#!/usr/bin/env python3
"""
Reddit Fetcher - Main Application Entry Point

This script interacts with the Reddit API to fetch the latest posts from a specified subreddit.
It demonstrates API authentication, data fetching, and proper error handling.
"""

import argparse
import sys
from config.settings import Settings
from core.auth import RedditAuthenticator
from services.reddit_service import RedditService
from presentation.console_formatter import ConsoleFormatter
from utils.logger import get_logger
from utils.error_handler import handle_application_error

logger = get_logger(__name__)

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Fetch latest posts from a subreddit')
    parser.add_argument('--subreddit', '-s', type=str, help='Subreddit name to fetch posts from')
    parser.add_argument('--limit', '-l', type=int, default=5, help='Number of posts to fetch (default: 5)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    return parser.parse_args()

def main():
    """Main application entry point."""
    try:
        # Parse command line arguments
        args = parse_arguments()
        
        # Initialize settings
        settings = Settings()
        settings.configure(
            subreddit=args.subreddit,
            post_limit=args.limit,
            verbose=args.verbose
        )
        
        # Initialize authenticator
        auth = RedditAuthenticator()
        reddit_instance = auth.authenticate()
        
        # Initialize services
        reddit_service = RedditService(reddit_instance)
        
        # Initialize presenters
        formatter = ConsoleFormatter()
        
        # Fetch and display posts
        subreddit_name = settings.subreddit
        post_limit = settings.post_limit
        
        logger.info(f"Fetching {post_limit} posts from r/{subreddit_name}")
        posts = reddit_service.get_latest_posts(subreddit_name, post_limit)
        
        # Format and display results
        formatter.display_posts(posts)
        
        logger.info("Process completed successfully")
        return 0
        
    except Exception as e:
        return handle_application_error(e)

if __name__ == "__main__":
    sys.exit(main())
