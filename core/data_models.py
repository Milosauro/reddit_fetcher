"""
Data Models module for the Reddit Fetcher application.

This module defines data structures for Reddit posts and other entities.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class RedditPost:
    """Data model representing a Reddit post."""
    
    id: str
    title: str
    author: str
    upvotes: int
    downvotes: Optional[int]
    score: int
    url: str
    created_utc: float
    num_comments: int
    is_self: bool
    selftext: Optional[str] = None
    
    @property
    def created_datetime(self) -> datetime:
        """Get the post creation time as a datetime object."""
        return datetime.fromtimestamp(self.created_utc)
    
    @classmethod
    def from_praw_submission(cls, submission):
        """
        Create a RedditPost instance from a PRAW submission object.
        
        Args:
            submission: PRAW submission object
            
        Returns:
            RedditPost: New RedditPost instance
        """
        return cls(
            id=submission.id,
            title=submission.title,
            author=submission.author.name if submission.author else "[deleted]",
            upvotes=submission.ups,
            downvotes=getattr(submission, 'downs', None),
            score=submission.score,
            url=submission.url,
            created_utc=submission.created_utc,
            num_comments=submission.num_comments,
            is_self=submission.is_self,
            selftext=submission.selftext if submission.is_self else None
        )
