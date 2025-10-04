"""
Tests for server functionality
"""

import pytest
from unittest.mock import patch, Mock

from src.server.handlers import SearchHandlers
from src.core.config import SearchException
from src.core.models import GeneralSearchResult


class TestSearchHandlers:
    """Test cases for SearchHandlers class."""
    
    def setup_method(self):
        self.handlers = SearchHandlers()
    
    def test_search_success(self):
        """Test successful search."""
        # Mock the client's search_general method directly
        mock_result = GeneralSearchResult(
            title='Test Result',
            url='http://example.com',
            content='Test content',
            score=0.95,
            category='general',
            author='Test Author'
        )
        
        with patch.object(self.handlers.client, 'search_general', return_value=[mock_result]):
            # Execute search
            result = self.handlers.search('test query', max_results=5)
            
            # Verify - results are now Pydantic models
            assert len(result) == 1
            assert result[0].title == 'Test Result'
            assert result[0].url == 'http://example.com'
            assert result[0].content == 'Test content'
            assert result[0].score == 0.95
    
    def test_search_max_results_validation(self):
        """Test max_results validation in search."""
        # Test upper limit
        with patch.object(self.handlers.client, 'search_general', return_value=[]):
            result = self.handlers.search('test', max_results=100)
            # Should not raise error, but limit max_results to 25
            assert isinstance(result, list)
        
        # Test lower limit
        with patch.object(self.handlers.client, 'search_general', return_value=[]):
            result = self.handlers.search('test', max_results=0)
            # Should not raise error, but set max_results to 1
            assert isinstance(result, list)
    
    @patch.object(SearchHandlers, '__init__', lambda x: None)
    @patch('src.server.handlers.SearxngClient')
    def test_search_exception_handling(self, mock_client_class):
        """Test search with search exception."""
        from fastmcp.exceptions import ToolError
        
        handlers = SearchHandlers()
        handlers.client = Mock()
        
        # Mock SearchException
        handlers.client.search_general.side_effect = SearchException("Search failed")
        
        # Execute search - should raise ToolError
        with pytest.raises(ToolError) as exc_info:
            handlers.search('test query')
        
        # Verify error message
        assert 'Search failed' in str(exc_info.value)
    
    @patch.object(SearchHandlers, '__init__', lambda x: None)
    @patch('src.server.handlers.SearxngClient')
    def test_search_unexpected_exception_handling(self, mock_client_class):
        """Test search with unexpected exception."""
        from fastmcp.exceptions import ToolError
        
        handlers = SearchHandlers()
        handlers.client = Mock()
        
        # Mock unexpected exception
        handlers.client.search_general.side_effect = ValueError("Unexpected error")
        
        # Execute search - should raise ToolError
        with pytest.raises(ToolError) as exc_info:
            handlers.search('test query')
        
        # Verify error message
        assert 'Unexpected error' in str(exc_info.value)
