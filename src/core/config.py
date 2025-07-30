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
    
    # Web fetching configuration
    MAX_CONTENT_LENGTH = 8000
    FETCH_TIMEOUT = 30.0
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"


class SearchException(Exception):
    """Custom exception for search-related errors."""
    pass


class SearchRequestException(SearchException):
    """Exception raised when search request fails."""
    pass


class SearchParseException(SearchException):
    """Exception raised when search response parsing fails."""
    pass