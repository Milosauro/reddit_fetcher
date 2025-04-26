"""
Tests for the post service module.
"""

import unittest
from datetime import datetime

from core.data_models import RedditPost
from services.post_service import PostService

class TestPostService(unittest.TestCase):
    """Test cases for the PostService class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.service = PostService()
        
        # Create some test posts
        self.posts = [
            RedditPost(
                id="post1",
                title="First post about Python",
                author="user1",
                upvotes=100,
                downvotes=10,
                score=90,
                url="https://reddit.com/r/test/post1",
                created_utc=1619430000,
                num_comments=20,
                is_self=True,
                selftext="This is a post about Python programming"
            ),
            RedditPost(
                id="post2",
                title="Second post about JavaScript",
                author="user2",
                upvotes=50,
                downvotes=5,
                score=45,
                url="https://reddit.com/r/test/post2",
                created_utc=1619433600,
                num_comments=10,
                is_self=True,
                selftext="This is a post about JavaScript"
            ),
            RedditPost(
                id="post3",
                title="Third post about cats",
                author="user3",
                upvotes=200,
                downvotes=20,
                score=180,
                url="https://reddit.com/r/test/post3",
                created_utc=1619437200,
                num_comments=30,
                is_self=True,
                selftext="This is a post about cute cats"
            )
        ]
        
    def test_filter_posts(self):
        """Test filtering posts with a custom function."""
        # Filter posts with "Python" in the title
        result = self.service.filter_posts(
            self.posts,
            lambda post: "Python" in post.title
        )
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, "post1")
        
    def test_sort_posts(self):
        """Test sorting posts by upvotes."""
        # Sort posts by upvotes in descending order
        result = self.service.sort_posts(
            self.posts,
            key_func=lambda post: post.upvotes,
            reverse=True
        )
        
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].id, "post3")  # Highest upvotes
        self.assertEqual(result[1].id, "post1")
        self.assertEqual(result[2].id, "post2")  # Lowest upvotes
        
    def test_search_posts(self):
        """Test searching posts for a query."""
        # Search for posts containing "Python"
        result = self.service.search_posts(self.posts, "Python")
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, "post1")
        
        # Case-insensitive search for "python"
        result = self.service.search_posts(self.posts, "python")
        self.assertEqual(len(result), 1)
        
        # Search in content
        result = self.service.search_posts(self.posts, "programming")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, "post1")
        
    def test_filter_by_min_upvotes(self):
        """Test filtering posts by minimum upvotes."""
        # Filter posts with at least 100 upvotes
        result = self.service.filter_by_min_upvotes(self.posts, 100)
        
        self.assertEqual(len(result), 2)
        self.assertIn("post1", [post.id for post in result])
        self.assertIn("post3", [post.id for post in result])
        
    def test_filter_by_min_comments(self):
        """Test filtering posts by minimum comment count."""
        # Filter posts with at least 20 comments
        result = self.service.filter_by_min_comments(self.posts, 20)
        
        self.assertEqual(len(result), 2)
        self.assertIn("post1", [post.id for post in result])
        self.assertIn("post3", [post.id for post in result])

if __name__ == '__main__':
    unittest.main()
