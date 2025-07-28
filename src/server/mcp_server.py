"""
FastMCP Server for exposing search functionality
Provides general web search capabilities via SearxNG
"""

import sys
from fastmcp import FastMCP
from .handlers import SearchHandlers


# Create the MCP server
mcp = FastMCP("Search Server")
handlers = SearchHandlers()


@mcp.tool
def web_search(query: str, max_results: int = 10, host: str = None):
    """
    Perform a general web search using SearxNG.
    
    Args:
        query: The search query to execute
        max_results: Maximum number of results to return (default: 10, max: 25)
        host: SearxNG server URL (uses SEARXNG_HOST env var if not specified)
        
    Returns:
        List of search results with title, url, content, score, category, and author
    """
    return handlers.web_search(query, max_results, host)


@mcp.tool  
def search_summary(query: str, max_results: int = 5, host: str = None):
    """
    Perform a web search and return a summary with key information.
    
    Args:
        query: The search query to execute
        max_results: Maximum number of results to analyze (default: 5, max: 15)
        host: SearxNG server URL (uses SEARXNG_HOST env var if not specified)
        
    Returns:
        Summary containing query info, result count, and top results with snippets
    """
    return handlers.search_summary(query, max_results, host)


def run_server():
    """Run the MCP server with appropriate transport."""
    # Check for HTTP mode flag
    if len(sys.argv) > 1 and sys.argv[1] == "--http":
        # Run with HTTP transport on port 3090
        mcp.run(transport="http", host="0.0.0.0", port=3090)
        print("Server running on http://localhost:3090")
    else:
        # Default stdio transport for MCP
        mcp.run()


if __name__ == "__main__":
    run_server()