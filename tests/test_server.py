"""
Unit tests for server functionality
"""

import unittest
from unittest.mock import patch, Mock

from src.server.handlers import SearchHandlers
from src.core.config import SearchException
from src.core.models import GeneralSearchResult


class TestSearchHandlers(unittest.TestCase):
    """Test cases for SearchHandlers class."""
    
    def setUp(self):
        self.handlers = SearchHandlers()
    
    def test_web_search_success(self):
        """Test successful web search."""
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
            result = self.handlers.web_search('test query', max_results=5)
            
            # Verify
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['title'], 'Test Result')
            self.assertEqual(result[0]['url'], 'http://example.com')
            self.assertEqual(result[0]['content'], 'Test content')
            self.assertEqual(result[0]['score'], 0.95)
            self.assertEqual(result[0]['category'], 'general')
            self.assertEqual(result[0]['author'], 'Test Author')
    
    @patch('src.server.handlers.SearxngClient')
    def test_web_search_with_custom_host(self, mock_client_class):
        """Test web search with custom host."""
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        mock_client.search_general.return_value = []
        
        # Execute search with custom host
        self.handlers.web_search('test query', host='http://custom:8080')
        
        # Verify custom client was created
        mock_client_class.assert_called_with('http://custom:8080')
    
    def test_web_search_max_results_validation(self):
        """Test max_results validation in web_search."""
        # Test upper limit
        with patch.object(self.handlers.client, 'search_general', return_value=[]):
            result = self.handlers.web_search('test', max_results=100)
            # Should not raise error, but limit max_results to 25
            self.assertIsInstance(result, list)
        
        # Test lower limit
        with patch.object(self.handlers.client, 'search_general', return_value=[]):
            result = self.handlers.web_search('test', max_results=0)
            # Should not raise error, but set max_results to 1
            self.assertIsInstance(result, list)
    
    @patch.object(SearchHandlers, '__init__', lambda x: None)
    @patch('src.server.handlers.SearxngClient')
    def test_web_search_search_exception(self, mock_client_class):
        """Test web search with search exception."""
        handlers = SearchHandlers()
        handlers.client = Mock()
        
        # Mock SearchException
        handlers.client.search_general.side_effect = SearchException("Search failed")
        
        # Execute search
        result = handlers.web_search('test query')
        
        # Verify error handling
        self.assertEqual(len(result), 1)
        self.assertIn('error', result[0])
        self.assertIn('Search failed', result[0]['error'])
    
    def test_search_summary_success(self):
        """Test successful search summary."""
        # Mock the client's search_general method directly
        mock_result = GeneralSearchResult(
            title='Test Result',
            url='http://example.com',
            content='This is a longer test content that should be truncated in the summary view.',
            category='general',
            author='Test Author'
        )
        
        with patch.object(self.handlers.client, 'search_general', return_value=[mock_result]):
            # Execute search
            result = self.handlers.search_summary('test query', max_results=5)
            
            # Verify summary structure
            self.assertIn('query', result)
            self.assertIn('total_results', result)
            self.assertIn('top_results', result)
            self.assertEqual(result['query'], 'test query')
            self.assertEqual(result['total_results'], 1)
            self.assertEqual(len(result['top_results']), 1)
            
            # Verify result details
            top_result = result['top_results'][0]
            self.assertEqual(top_result['rank'], 1)
            self.assertEqual(top_result['title'], 'Test Result')
            self.assertEqual(top_result['url'], 'http://example.com')
            self.assertTrue(len(top_result['snippet']) <= 203)  # 200 chars + "..."
            self.assertEqual(top_result['category'], 'general')
            self.assertEqual(top_result['author'], 'Test Author')
    
    def test_search_summary_max_results_validation(self):
        """Test max_results validation in search_summary."""
        # Test upper limit
        with patch.object(self.handlers.client, 'search_general', return_value=[]):
            result = self.handlers.search_summary('test', max_results=100)
            # Should not raise error, but limit max_results to 15
            self.assertIsInstance(result, dict)
        
        # Test lower limit  
        with patch.object(self.handlers.client, 'search_general', return_value=[]):
            result = self.handlers.search_summary('test', max_results=0)
            # Should not raise error, but set max_results to 1
            self.assertIsInstance(result, dict)
    
    @patch.object(SearchHandlers, '__init__', lambda x: None)
    @patch('src.server.handlers.SearxngClient')
    def test_search_summary_search_exception(self, mock_client_class):
        """Test search summary with search exception."""
        handlers = SearchHandlers()
        handlers.client = Mock()
        
        # Mock SearchException
        handlers.client.search_general.side_effect = SearchException("Search failed")
        
        # Execute search
        result = handlers.search_summary('test query')
        
        # Verify error handling
        self.assertIn('error', result)
        self.assertIn('query', result)
        self.assertIn('Search failed', result['error'])
        self.assertEqual(result['query'], 'test query')


if __name__ == '__main__':
    unittest.main()