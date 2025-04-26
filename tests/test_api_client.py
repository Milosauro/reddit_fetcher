"""
Tests for the Reddit API client module.
"""

import unittest
from unittest.mock import MagicMock, patch

import praw

from core.api_client import RedditClient
from utils.error_handler import RedditAPIError, RateLimitError

class TestRedditClient(unittest.TestCase):
    """Test cases for the RedditClient class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_reddit = MagicMock()
        self.client = RedditClient(self.mock_reddit)
        
    def test_get_subreddit(self):
        """Test getting a subreddit."""
        # Arrange
        mock_subreddit = MagicMock()
        self.mock_reddit.subreddit.return_value = mock_subreddit
        
        # Act
        result = self.client.get_subreddit("python")
        
        # Assert
        self.mock_reddit.subreddit.assert_called_once_with("python")
        self.assertEqual(result, mock_subreddit)
        
    def test_get_subreddit_error(self):
        """Test error handling when getting a subreddit."""
        # Arrange
        self.mock_reddit.subreddit.side_effect = Exception("API Error")
        
        # Act & Assert
        with self.assertRaises(RedditAPIError):
            self.client.get_subreddit("nonexistent")
            
    @patch('time.sleep')  # Mock sleep to avoid waiting in tests
    def test_get_latest_posts_rate_limit(self, mock_sleep):
        """Test rate limit handling when getting posts."""
        # Arrange
        mock_subreddit = MagicMock()
        self.mock_reddit.subreddit.return_value = mock_subreddit
        
        # Create a simple Exception with 'rate limit' in the message to match the detection in the method
        rate_limit_error = Exception("rate limit exceeded")
        mock_subreddit.new.side_effect = [rate_limit_error, [MagicMock(), MagicMock()]]
        
        # Act
        result = self.client.get_latest_posts("python", 2)
        
        # Assert
        self.assertEqual(len(result), 2)
        mock_sleep.assert_called_once()
        
    def test_get_latest_posts_success(self):
        """Test successfully getting latest posts."""
        # Arrange
        mock_subreddit = MagicMock()
        self.mock_reddit.subreddit.return_value = mock_subreddit
        
        mock_posts = [MagicMock(), MagicMock()]
        mock_subreddit.new.return_value = mock_posts
        
        # Act
        result = self.client.get_latest_posts("python", 2)
        
        # Assert
        self.assertEqual(result, mock_posts)
        mock_subreddit.new.assert_called_once_with(limit=2)

if __name__ == '__main__':
    unittest.main()
