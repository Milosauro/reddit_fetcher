#!/usr/bin/env python3
"""
Example script demonstrating how to use Reddit Fetcher as a library.

This script shows how to use the core functionality of Reddit Fetcher
in your own Python applications.
"""

import os
import sys
from dotenv import load_dotenv

# Add parent directory to path to allow imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Load environment variables from .env file
load_dotenv()

# Import Reddit Fetcher modules
from core.auth import RedditAuthenticator
from services.reddit_service import RedditService
from services.post_service import PostService
from presentation.console_formatter import ConsoleFormatter
from presentation.output_manager import OutputManager

def main():
    """
    Example usage of Reddit Fetcher as a library.
    """
    # Step 1: Authenticate with Reddit API
    print("Authenticating with Reddit API...")
    auth = RedditAuthenticator()
    reddit = auth.authenticate()
    
    # Step 2: Initialize services
    reddit_service = RedditService(reddit)
    post_service = PostService()
    
    # Step 3: Fetch posts from a subreddit
    subreddit = "python"  # Change to any subreddit you want
    limit = 5
    
    print(f"Fetching {limit} posts from r/{subreddit}...")
    posts = reddit_service.get_latest_posts(subreddit, limit)
    
    # Step 4: Process posts (optional)
    # Example 1: Sort posts by upvotes (highest first)
    sorted_posts = post_service.sort_posts(
        posts, 
        key_func=lambda post: post.upvotes,
        reverse=True
    )
    
    # Example 2: Filter posts with at least 10 upvotes
    filtered_posts = post_service.filter_by_min_upvotes(posts, 10)
    
    # Example 3: Search posts for a specific term
    search_term = "python"
    searched_posts = post_service.search_posts(posts, search_term)
    
    # Step 5: Display posts
    formatter = ConsoleFormatter()
    
    print("\nAll Posts:")
    formatter.display_posts(posts)
    
    print("\nSorted Posts (by upvotes):")
    formatter.display_posts(sorted_posts)
    
    print(f"\nFiltered Posts (min 10 upvotes):")
    formatter.display_posts(filtered_posts)
    
    print(f"\nSearch Results for '{search_term}':")
    formatter.display_posts(searched_posts)
    
    # Step 6: Export posts to JSON (optional)
    output_manager = OutputManager()
    output_file = "posts.json"
    output_manager.export_to_json(posts, output_file)
    print(f"\nPosts exported to {output_file}")

if __name__ == "__main__":
    main()
