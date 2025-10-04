"""
FastMCP Server for exposing search functionality
Provides general web search capabilities via SearxNG
"""

import argparse
import sys
from typing import Any, Dict, Annotated
from fastmcp import FastMCP
from .handlers import SearchHandlers


# Create the MCP server
mcp = FastMCP("Search Server")
handlers = SearchHandlers()


@mcp.tool
def search(
    query: Annotated[str, "The search query to execute"],
    max_results: Annotated[int, "Maximum number of results to return (default: 10, max: 25)"] = 10
):
    """
    Perform a general web search using SearxNG.
    
    Returns:
        List of search results with title, url, content, score
    """
    return handlers.search(query, max_results)


@mcp.tool
def search_videos(
    query: Annotated[str, "The video search query to execute"],
    max_results: Annotated[int, "Maximum number of results to return (default: 10, max: 20)"] = 10
):
    """
    Search for YouTube videos using SearxNG.
    
    Returns:
        List of video results, each containing:
        - url: YouTube video URL
        - title: Video title
        - author: Channel name
        - content: Video description/summary
        - length: Video duration (e.g., "02:02:21")
    """
    return handlers.search_videos(query, max_results)


@mcp.tool(
    name="fetch_content",
    tags={"web", "fetch"},
    enabled=True,
)
async def fetch_content(
    url: Annotated[str, "The webpage URL to fetch content from"],
    offset: Annotated[int, "Starting position for content retrieval (use 'next_offset' from previous response)"] = 0
) -> Dict[str, Any]:
    """
    Fetch and parse content from a webpage URL with pagination support.
    
    Content is retrieved in chunks of 30,000 characters. If content is truncated,
    use the returned 'next_offset' value in a subsequent call to retrieve the next chunk.
    
    Returns:
        Dictionary containing:
        - content: The parsed text content (up to 30,000 characters)
        - content_length: Length of the returned content chunk
        - is_truncated: Boolean indicating if more content is available
        - offset: The offset used for this request
        - next_offset: The offset to use for the next request (None if not truncated)
        - total_length: Total length of the full content
        - success: Boolean indicating if the fetch was successful
    """
    return await handlers.fetch_content(url, offset)


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
