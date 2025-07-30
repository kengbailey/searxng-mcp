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
def search(query: str, max_results: int = 10):
    """
    Perform a general web search using SearxNG.
    
    Args:
        query: The search query to execute
        max_results: Maximum number of results to return (default: 10, max: 25)
        
    Returns:
        List of search results with title, url, content, score
    """
    return handlers.search(query, max_results)


@mcp.tool
async def fetch_content(url: str):
    """
    Fetch and parse content from a webpage URL.
    
    Args:
        url: The webpage URL to fetch content from
        
    Returns:
        Dictionary containing parsed content and metadata
    """
    return await handlers.fetch_content(url)


def run_server():
    """Run the MCP server with appropriate transport."""
    # Check for HTTP mode flag
    if len(sys.argv) > 1 and sys.argv[1] == "--http":
        # Run with HTTP transport on port 3090
        mcp.run(transport="http", host="0.0.0.0", port=3090)
        print("Server running on http://0.0.0.0:3090")
    else:
        # Default stdio transport for MCP
        mcp.run()


if __name__ == "__main__":
    run_server()