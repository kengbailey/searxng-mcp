"""
Configuration management for SearxNG search
"""

import os


class SearchConfig:
    """Configuration settings for search functionality."""
    
    # Default SearxNG host
    DEFAULT_SEARXNG_HOST = os.getenv('SEARXNG_HOST', 'http://berry:8189')
    
    # Request timeout settings
    REQUEST_TIMEOUT = 10
    
    # Result limits
    MAX_GENERAL_RESULTS = 25
    MAX_VIDEO_RESULTS = 20
    MAX_SUMMARY_RESULTS = 15
    
    # Default result counts
    DEFAULT_GENERAL_RESULTS = 15
    DEFAULT_VIDEO_RESULTS = 10
    DEFAULT_SUMMARY_RESULTS = 5


class SearchException(Exception):
    """Custom exception for search-related errors."""
    pass


class SearchRequestException(SearchException):
    """Exception raised when search request fails."""
    pass


class SearchParseException(SearchException):
    """Exception raised when search response parsing fails."""
    pass