"""
Tests for video search functionality
"""

import pytest
from src.server.handlers import SearchHandlers
from src.core.config import SearchConfig


class TestVideoSearch:
    """Test cases for video search."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.handlers = SearchHandlers()
    
    def test_search_videos_basic(self):
        """Test basic video search functionality."""
        query = "python tutorial"
        results = self.handlers.search_videos(query, max_results=5)
        
        # Should return a list
        assert isinstance(results, list)
        assert len(results) > 0
        assert len(results) <= 5
        
        # Check first result structure
        if results:
            first_result = results[0]
            assert hasattr(first_result, 'url')
            assert hasattr(first_result, 'title')
            assert hasattr(first_result, 'author')
            assert hasattr(first_result, 'content')
            assert hasattr(first_result, 'length')
            
            # URL should be YouTube
            assert "youtube.com" in first_result.url
    
    def test_search_videos_max_results_validation(self):
        """Test that max_results is properly validated."""
        query = "coding"
        
        # Test with value above max
        results = self.handlers.search_videos(query, max_results=100)
        assert len(results) <= SearchConfig.MAX_VIDEO_RESULTS
        
        # Test with value below 1
        results = self.handlers.search_videos(query, max_results=0)
        assert len(results) >= 1
    
    def test_search_videos_response_fields(self):
        """Test that all expected fields are present in response."""
        query = "machine learning"
        results = self.handlers.search_videos(query, max_results=3)
        
        if results:
            for result in results:
                # All required fields should be present
                assert hasattr(result, 'url')
                assert hasattr(result, 'title')
                assert hasattr(result, 'author')
                assert hasattr(result, 'content')
                assert hasattr(result, 'length')
                
                # Types should be correct
                assert isinstance(result.url, str)
                assert isinstance(result.title, str)
                # author and content can be None
                if result.length is not None:
                    assert isinstance(result.length, (str, float))
