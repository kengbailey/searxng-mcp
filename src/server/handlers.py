"""
MCP tool handlers for search functionality
"""

from typing import List, Dict, Any
from ..core.search import SearxngClient
from ..core.web_fetcher import WebContentFetcher
from ..core.config import SearchConfig, SearchException


class SearchHandlers:
    """Handlers for MCP search tools."""
    
    def __init__(self):
        self.client = SearxngClient()
        self.fetcher = WebContentFetcher()
    
    def search(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Perform a general web search using SearxNG.
        
        Args:
            query: The search query to execute
            max_results: Maximum number of results to return (default: 10, max: 25)
            
        Returns:
            List of search results with title, url, content, score, category, and author
        """
        # Validate max_results
        if max_results > SearchConfig.MAX_GENERAL_RESULTS:
            max_results = SearchConfig.MAX_GENERAL_RESULTS
        elif max_results < 1:
            max_results = 1
        
        try:
            # Call the search function
            results = self.client.search_general(query, max_results=max_results)
            
            # Convert Pydantic models to dictionaries for JSON serialization
            return [
                {
                    "title": result.title,
                    "url": result.url,
                    "content": result.content,
                    "score": result.score,
                }
                for result in results
            ]
        except SearchException as e:
            # Return an error result that the LLM can understand
            return [{"error": f"Search failed: {str(e)}"}]
        except Exception as e:
            # Handle unexpected errors
            return [{"error": f"Unexpected error: {str(e)}"}]
    
    async def fetch_content(self, url: str, offset: int = 0) -> Dict[str, Any]:
        """
        Fetch and parse content from a webpage URL with pagination support.
        
        Args:
            url: The webpage URL to fetch content from
            offset: Starting position for content retrieval (default: 0)
            
        Returns:
            Dictionary containing the parsed content, pagination metadata, or error information
        """
        try:
            content, is_truncated, next_offset, total_length = await self.fetcher.fetch_and_parse(url, offset)
            return {
                "content": content,
                "content_length": len(content),
                "is_truncated": is_truncated,
                "offset": offset,
                "next_offset": next_offset if is_truncated else None,
                "total_length": total_length,
                "success": True
            }
        except SearchException as e:
            return {
                "url": url,
                "error": str(e),
                "success": False
            }
        except Exception as e:
            return {
                "url": url,
                "error": f"Unexpected error: {str(e)}",
                "success": False
            }
