"""
Unit tests for core search functionality
"""

import unittest
from unittest.mock import patch, Mock
import requests

from src.core.search import SearxngClient, search_general, search_videos
from src.core.config import SearchRequestException, SearchParseException
from src.core.models import RawSearxngResponse, RawResult


class TestSearxngClient(unittest.TestCase):
    """Test cases for SearxngClient class."""
    
    def setUp(self):
        self.client = SearxngClient()
    
    def test_init_default_host(self):
        """Test client initialization with default host."""
        client = SearxngClient()
        self.assertIn('berry:8189', client.host)
    
    def test_init_custom_host(self):
        """Test client initialization with custom host."""
        custom_host = "http://example.com:8080"
        client = SearxngClient(custom_host)
        self.assertEqual(client.host, custom_host)
    
    @patch('src.core.search.requests.get')
    def test_search_raw_success(self, mock_get):
        """Test successful raw search."""
        # Mock response
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            'query': 'test query',
            'number_of_results': 1,
            'results': [{
                'url': 'http://example.com',
                'title': 'Test Result',
                'engine': 'test'
            }]
        }
        mock_get.return_value = mock_response
        
        # Execute search
        result = self.client._search_raw('test query')
        
        # Verify
        self.assertIsInstance(result, RawSearxngResponse)
        self.assertEqual(result.query, 'test query')
        self.assertEqual(len(result.results), 1)
        self.assertEqual(result.results[0].title, 'Test Result')
    
    @patch('src.core.search.requests.get')
    def test_search_raw_request_failure(self, mock_get):
        """Test search request failure."""
        mock_get.side_effect = requests.exceptions.RequestException("Network error")
        
        with self.assertRaises(SearchRequestException):
            self.client._search_raw('test query')
    
    @patch('src.core.search.requests.get')
    def test_search_raw_parse_failure(self, mock_get):
        """Test search response parsing failure."""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response
        
        with self.assertRaises(SearchParseException):
            self.client._search_raw('test query')
    
    @patch.object(SearxngClient, '_search_raw')
    def test_search_general_success(self, mock_search_raw):
        """Test successful general search."""
        # Mock raw response
        mock_raw_result = RawResult(
            url='http://example.com',
            title='Test Result',
            content='Test content',
            engine='test',
            score=0.95,
            category='general'
        )
        mock_response = RawSearxngResponse(
            query='test query',
            number_of_results=1,
            results=[mock_raw_result]
        )
        mock_search_raw.return_value = mock_response
        
        # Execute search
        results = self.client.search_general('test query')
        
        # Verify
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, 'Test Result')
        self.assertEqual(results[0].url, 'http://example.com')
        self.assertEqual(results[0].content, 'Test content')
        self.assertEqual(results[0].score, 0.95)
    
    @patch.object(SearxngClient, '_search_raw')
    def test_search_videos_success(self, mock_search_raw):
        """Test successful video search."""
        # Mock raw response
        mock_raw_result = RawResult(
            url='http://youtube.com/watch?v=test',
            title='Test Video',
            content='Test video description',
            engine='youtube',
            author='Test Author',
            duration='5:30',
            publishedDate='2024-01-01'
        )
        mock_response = RawSearxngResponse(
            query='test video query',
            number_of_results=1,
            results=[mock_raw_result]
        )
        mock_search_raw.return_value = mock_response
        
        # Execute search
        results = self.client.search_videos('test video query')
        
        # Verify
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, 'Test Video')
        self.assertEqual(results[0].url, 'http://youtube.com/watch?v=test')
        self.assertEqual(results[0].author, 'Test Author')
        self.assertEqual(results[0].duration, '5:30')
        self.assertEqual(results[0].published_date, '2024-01-01')


class TestConvenienceFunctions(unittest.TestCase):
    """Test cases for convenience functions."""
    
    @patch.object(SearxngClient, 'search_general')
    def test_search_general_function(self, mock_search_general):
        """Test search_general convenience function."""
        mock_search_general.return_value = []
        
        result = search_general('test query')
        
        mock_search_general.assert_called_once_with('test query', None)
        self.assertEqual(result, [])
    
    @patch.object(SearxngClient, 'search_videos')
    def test_search_videos_function(self, mock_search_videos):
        """Test search_videos convenience function."""
        mock_search_videos.return_value = []
        
        result = search_videos('test query')
        
        mock_search_videos.assert_called_once_with('test query', 'youtube', None)
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()