"""
Tests for the data models module.
"""

import unittest
from unittest.mock import MagicMock
from datetime import datetime

from core.data_models import RedditPost

class TestRedditPost(unittest.TestCase):
    """Test cases for the RedditPost data model."""
    
    def test_created_datetime(self):
        """Test the created_datetime property."""
        # Arrange
        timestamp = 1619430000  # April 26, 2021 10:00:00 UTC
        post = RedditPost(
            id="abc123",
            title="Test Post",
            author="testuser",
            upvotes=100,
            downvotes=10,
            score=90,
            url="https://reddit.com/r/test/comments/abc123",
            created_utc=timestamp,
            num_comments=5,
            is_self=True,
            selftext="This is a test post"
        )
        
        # Act
        result = post.created_datetime
        
        # Assert
        self.assertIsInstance(result, datetime)
        self.assertEqual(result.year, 2021)
        self.assertEqual(result.month, 4)
        self.assertEqual(result.day, 26)
        
    def test_from_praw_submission(self):
        """Test creating a post from a PRAW submission."""
        # Arrange
        mock_submission = MagicMock()
        mock_submission.id = "abc123"
        mock_submission.title = "Test Post"
        mock_submission.author.name = "testuser"
        mock_submission.ups = 100
        mock_submission.score = 90
        mock_submission.url = "https://reddit.com/r/test/comments/abc123"
        mock_submission.created_utc = 1619430000
        mock_submission.num_comments = 5
        mock_submission.is_self = True
        mock_submission.selftext = "This is a test post"
        
        # Act
        post = RedditPost.from_praw_submission(mock_submission)
        
        # Assert
        self.assertEqual(post.id, "abc123")
        self.assertEqual(post.title, "Test Post")
        self.assertEqual(post.author, "testuser")
        self.assertEqual(post.upvotes, 100)
        self.assertEqual(post.score, 90)
        self.assertEqual(post.url, "https://reddit.com/r/test/comments/abc123")
        self.assertEqual(post.created_utc, 1619430000)
        self.assertEqual(post.num_comments, 5)
        self.assertTrue(post.is_self)
        self.assertEqual(post.selftext, "This is a test post")
        
    def test_from_praw_submission_deleted_author(self):
        """Test handling of deleted authors."""
        # Arrange
        mock_submission = MagicMock()
        mock_submission.id = "abc123"
        mock_submission.title = "Test Post"
        mock_submission.author = None  # Deleted author
        mock_submission.ups = 100
        mock_submission.score = 90
        mock_submission.url = "https://reddit.com/r/test/comments/abc123"
        mock_submission.created_utc = 1619430000
        mock_submission.num_comments = 5
        mock_submission.is_self = False
        mock_submission.selftext = ""
        
        # Act
        post = RedditPost.from_praw_submission(mock_submission)
        
        # Assert
        self.assertEqual(post.author, "[deleted]")
        self.assertFalse(post.is_self)
        self.assertIsNone(post.selftext)

if __name__ == '__main__':
    unittest.main()
