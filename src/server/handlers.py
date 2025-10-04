"""
MCP tool handlers for search functionality
"""

from typing import List, Dict, Any
from fastmcp.exceptions import ToolError
from ..core.search import SearxngClient
from ..core.web_fetcher import WebContentFetcher
from ..core.config import SearchConfig, SearchException
from ..core.models import SearchResultOutput, VideoSearchResultOutput, FetchContentOutput


class SearchHandlers:
    """Handlers for MCP search tools."""
    
    def __init__(self):
        self.client = SearxngClient()
        self.fetcher = WebContentFetcher()
    
    def search(self, query: str, max_results: int = 10) -> List[SearchResultOutput]:
        """
        Perform a general web search using SearxNG.
        
        Args:
            query: The search query to execute
            max_results: Maximum number of results to return (default: 10, max: 25)
            
        Returns:
            List of search results with title, url, content, score
        """
        # Validate query
        if not query or not query.strip():
            raise ToolError("Search query cannot be empty")
        
        # Validate max_results
        if max_results > SearchConfig.MAX_GENERAL_RESULTS:
            max_results = SearchConfig.MAX_GENERAL_RESULTS
        elif max_results < 1:
            max_results = 1
        
        try:
            # Call the search function
            results = self.client.search_general(query, max_results=max_results)
            
            # Convert to output models
            return [
                SearchResultOutput(
                    title=result.title,
                    url=result.url,
                    content=result.content,
                    score=result.score or 0.0,
                )
                for result in results
            ]
        except SearchException as e:
            raise ToolError(f"Search failed: {str(e)}")
        except Exception as e:
            raise ToolError(f"Unexpected error: {str(e)}")
    
    def search_videos(self, query: str, max_results: int = 10) -> List[VideoSearchResultOutput]:
        """
        Search for YouTube videos using SearxNG.
        
        Args:
            query: The search query to execute
            max_results: Maximum number of results to return (default: 10, max: 20)
            
        Returns:
            List of video results with url, title, author, content, and length
        """
        # Validate query
        if not query or not query.strip():
            raise ToolError("Video search query cannot be empty")
        
        # Validate max_results
        if max_results > SearchConfig.MAX_VIDEO_RESULTS:
            max_results = SearchConfig.MAX_VIDEO_RESULTS
        elif max_results < 1:
            max_results = 1
        
        try:
            # Call the video search function (YouTube only)
            results = self.client.search_videos(query, engines='youtube', max_results=max_results)
            
            # Convert to output models
            return [
                VideoSearchResultOutput(
                    url=result.url,
                    title=result.title,
                    author=result.author,
                    content=result.content,
                    length=result.duration,
                )
                for result in results
            ]
        except SearchException as e:
            raise ToolError(f"Video search failed: {str(e)}")
        except Exception as e:
            raise ToolError(f"Unexpected error: {str(e)}")
    
    async def fetch_content(self, url: str, offset: int = 0) -> FetchContentOutput:
        """
        Fetch and parse content from a webpage URL with pagination support.
        
        Args:
            url: The webpage URL to fetch content from
            offset: Starting position for content retrieval (default: 0)
            
        Returns:
            FetchContentOutput containing the parsed content and pagination metadata
        """
        # Validate URL
        if not url or not url.strip():
            raise ToolError("URL cannot be empty")
        
        try:
            content, is_truncated, next_offset, total_length = await self.fetcher.fetch_and_parse(url, offset)
            return FetchContentOutput(
                content=content,
                content_length=len(content),
                is_truncated=is_truncated,
                offset=offset,
                next_offset=next_offset if is_truncated else None,
                total_length=total_length,
                success=True
            )
        except SearchException as e:
            raise ToolError(f"Failed to fetch content: {str(e)}")
        except Exception as e:
            raise ToolError(f"Unexpected error: {str(e)}")
