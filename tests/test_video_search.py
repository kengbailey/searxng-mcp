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
        if results and "error" not in results[0]:
            first_result = results[0]
            assert "url" in first_result
            assert "title" in first_result
            assert "author" in first_result
            assert "content" in first_result
            assert "length" in first_result
            
            # URL should be YouTube
            assert "youtube.com" in first_result["url"]
    
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
        
        if results and "error" not in results[0]:
            for result in results:
                # All required fields should be present
                assert "url" in result
                assert "title" in result
                assert "author" in result
                assert "content" in result
                assert "length" in result
                
                # Types should be correct
                assert isinstance(result["url"], str)
                assert isinstance(result["title"], str)
                # author and content can be None
                if result["length"] is not None:
                    assert isinstance(result["length"], (str, float))
