"""
Tests for web content fetching functionality
"""

import pytest
import asyncio
from src.core.web_fetcher import WebContentFetcher
from src.core.config import SearchException


class TestWebContentFetcher:
    """Test cases for WebContentFetcher."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.fetcher = WebContentFetcher()
    
    @pytest.mark.asyncio
    async def test_fetch_valid_url(self):
        """Test fetching from a valid URL."""
        # Use a reliable test URL
        url = "https://httpbin.org/html"
        
        content, _ = await self.fetcher.fetch_and_parse(url)
        
        assert isinstance(content, str)
        assert len(content) > 0
        assert "Herman Melville" in content  # httpbin.org/html contains this
    
    @pytest.mark.asyncio
    async def test_fetch_invalid_url(self):
        """Test handling of invalid URL."""
        url = "https://this-domain-does-not-exist-12345.com"
        
        with pytest.raises(SearchException):
            await self.fetcher.fetch_and_parse(url)
    
    @pytest.mark.asyncio
    async def test_content_truncation(self):
        """Test that long content gets truncated."""
        # This test would require a reliable URL with very long content
        # For now, we can test the truncation logic by mocking or
        # using a known URL with substantial content
        pass
    
    @pytest.mark.asyncio
    async def test_content_cleaning(self):
        """Test that HTML content is properly cleaned."""
        # httpbin.org/html has known HTML structure
        url = "https://httpbin.org/html"
        
        content, _ = await self.fetcher.fetch_and_parse(url)
        
        # Should not contain HTML tags
        assert "<" not in content
        assert ">" not in content
        
        # Should contain readable text
        assert len(content.strip()) > 0
    
    @pytest.mark.asyncio
    async def test_fetch_pdf_content(self):
        """Test fetching and parsing PDF content using a real PDF URL."""        
        pdf_url = "https://s28.q4cdn.com/823357996/files/doc_financials/2025/q1/DNA-Q1-2025-10Q.pdf"
        text, is_truncated = await self.fetcher.fetch_and_parse(pdf_url)
        
        # Basic assertions
        assert text is not None
        assert isinstance(text, str)
        assert len(text) > 0
        
        # Should contain some expected financial document content
        text_lower = text.lower()
        assert any(term in text_lower for term in ["financial", "quarterly", "revenue", "10-q"])
        
        # Check truncation flag is boolean
        assert isinstance(is_truncated, bool)