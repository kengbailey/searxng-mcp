"""
MCP tool handlers for search functionality
"""

from typing import List, Dict, Any
from ..core.search import SearxngClient
from ..core.config import SearchConfig, SearchException


class SearchHandlers:
    """Handlers for MCP search tools."""
    
    def __init__(self):
        self.client = SearxngClient()
    
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