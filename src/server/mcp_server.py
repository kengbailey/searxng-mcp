"""
FastMCP Server for exposing search functionality
Provides general web search capabilities via SearxNG
"""

import argparse
import sys
from typing import Any, Dict
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


@mcp.tool(
    name="fetch_content",
    tags={"web", "fetch"},
    enabled=True,
)
async def fetch_content(url: str) -> Dict[str, Any]:
    """
    Fetch and parse content from a webpage URL.
    
    Args:
        url: The webpage URL to fetch content from
        
    Returns:
        Dictionary containing parsed content and metadata
    """
    return await handlers.fetch_content(url)


def run_server():
    """Run the MCP server with appropriate transport and configurable port."""
    # args
    parser = argparse.ArgumentParser(description="Run MCP server with configurable transport and port")
    parser.add_argument('--port', type=int, default=3090, help='Port number for HTTP transport (default: 3090)')
    parser.add_argument('--http', action='store_true', help='Run server with HTTP transport')
    parser.add_argument('--sse', action='store_true', help='Run server with SSE transport')
    args = parser.parse_args()

    # Run server with appropriate transport and port
    if args.http:
        mcp.run(transport="http", host="0.0.0.0", port=args.port)
        print(f"Server running on http://0.0.0.0:{args.port} with HTTP transport")
    elif args.sse:
        mcp.run(transport="sse", host="0.0.0.0", port=args.port)
        print(f"Server running on http://0.0.0.0:{args.port} with SSE transport")
    else:
        mcp.run(transport="http", host="0.0.0.0", port=args.port)
        print(f"Server running on http://0.0.0.0:{args.port} with HTTP transport")



if __name__ == "__main__":
    run_server()