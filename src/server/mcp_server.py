"""
FastMCP Server for exposing search functionality
Provides general web search capabilities via SearxNG
"""

import argparse
import sys
from typing import List, Annotated
from pydantic import Field
from fastmcp import FastMCP
from .handlers import SearchHandlers
from ..core.models import SearchResultOutput, VideoSearchResultOutput, FetchContentOutput


# Create the MCP server
mcp = FastMCP("WebIntel MCP")
handlers = SearchHandlers()


@mcp.tool(
    tags={"search", "web"},
    annotations={
        "title": "Web Search",
        "readOnlyHint": True,
        "openWorldHint": True,
        "idempotentHint": True
    }
)
def search(
    query: Annotated[str, Field(
        description="The search query to execute",
        min_length=1,
        max_length=500
    )],
    max_results: Annotated[int, Field(
        description="Maximum number of results to return (default: 10, min: 1, max: 25)",
        ge=1,
        le=25
    )] = 10
) -> List[SearchResultOutput]:
    """
    Perform a general web search using SearxNG.
    
    Returns:
        List of search results with title, url, content, score
    """
    return handlers.search(query, max_results)


@mcp.tool(
    tags={"search", "video", "youtube"},
    annotations={
        "title": "YouTube Video Search",
        "readOnlyHint": True,
        "openWorldHint": True,
        "idempotentHint": True
    }
)
def search_videos(
    query: Annotated[str, Field(
        description="The video search query to execute",
        min_length=1,
        max_length=500
    )],
    max_results: Annotated[int, Field(
        description="Maximum number of results to return (default: 10, min: 1, max: 20)",
        ge=1,
        le=20
    )] = 10
) -> List[VideoSearchResultOutput]:
    """
    Search for YouTube videos using SearxNG.
    
    Returns:
        List of video results with url, title, author, content, and length
    """
    return handlers.search_videos(query, max_results)


@mcp.tool(
    name="fetch_content",
    tags={"web", "fetch", "content"},
    annotations={
        "title": "Fetch Web Content",
        "readOnlyHint": True,
        "openWorldHint": True,
        "idempotentHint": False
    }
)
async def fetch_content(
    url: Annotated[str, Field(
        description="The webpage URL to fetch content from",
        min_length=1
    )],
    offset: Annotated[int, Field(
        description="Starting position for content retrieval (default: 0, min: 0). Use 'next_offset' from previous response",
        ge=0
    )] = 0
) -> FetchContentOutput:
    """
    Fetch and parse content from a webpage URL with pagination support.
    
    Content is retrieved in chunks of 30,000 characters. If content is truncated,
    use the returned 'next_offset' value in a subsequent call to retrieve the next chunk.
    
    Returns:
        FetchContentOutput with parsed content and pagination metadata
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
