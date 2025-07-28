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
    
    def web_search(self, query: str, max_results: int = 10, host: str = None) -> List[Dict[str, Any]]:
        """
        Perform a general web search using SearxNG.
        
        Args:
            query: The search query to execute
            max_results: Maximum number of results to return (default: 10, max: 25)
            host: SearxNG server URL (uses SEARXNG_HOST env var if not specified)
            
        Returns:
            List of search results with title, url, content, score, category, and author
        """
        # Validate max_results
        if max_results > SearchConfig.MAX_GENERAL_RESULTS:
            max_results = SearchConfig.MAX_GENERAL_RESULTS
        elif max_results < 1:
            max_results = 1
        
        try:
            # Use different client if host is provided
            if host:
                client = SearxngClient(host)
            else:
                client = self.client
            
            # Call the search function
            results = client.search_general(query, max_results=max_results)
            
            # Convert Pydantic models to dictionaries for JSON serialization
            return [
                {
                    "title": result.title,
                    "url": result.url,
                    "content": result.content,
                    "score": result.score,
                    "category": result.category,
                    "author": result.author
                }
                for result in results
            ]
        except SearchException as e:
            # Return an error result that the LLM can understand
            return [{"error": f"Search failed: {str(e)}"}]
        except Exception as e:
            # Handle unexpected errors
            return [{"error": f"Unexpected error: {str(e)}"}]
    
    def search_summary(self, query: str, max_results: int = 5, host: str = None) -> Dict[str, Any]:
        """
        Perform a web search and return a summary with key information.
        
        Args:
            query: The search query to execute
            max_results: Maximum number of results to analyze (default: 5, max: 15)
            host: SearxNG server URL (uses SEARXNG_HOST env var if not specified)
            
        Returns:
            Summary containing query info, result count, and top results with snippets
        """
        # Validate max_results for summary (smaller limit)
        if max_results > SearchConfig.MAX_SUMMARY_RESULTS:
            max_results = SearchConfig.MAX_SUMMARY_RESULTS
        elif max_results < 1:
            max_results = 1
        
        try:
            # Use different client if host is provided
            if host:
                client = SearxngClient(host)
            else:
                client = self.client
            
            # Call the search function
            results = client.search_general(query, max_results=max_results)
            
            # Create a summary format
            summary = {
                "query": query,
                "total_results": len(results),
                "top_results": []
            }
            
            for i, result in enumerate(results, 1):
                # Truncate content for summary view
                content_snippet = ""
                if result.content:
                    content_snippet = result.content[:200] + "..." if len(result.content) > 200 else result.content
                
                summary["top_results"].append({
                    "rank": i,
                    "title": result.title,
                    "url": result.url,
                    "snippet": content_snippet,
                    "category": result.category,
                    "author": result.author
                })
            
            return summary
            
        except SearchException as e:
            return {"error": f"Search failed: {str(e)}", "query": query}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}", "query": query}