"""
FastMCP Server for exposing search functionality
Provides general web search capabilities via SearxNG
"""

import os
from fastmcp import FastMCP
from typing import List, Dict, Any
from app import search_general, GeneralSearchResult, DEFAULT_SEARXNG_HOST
import json

# Create the MCP server
mcp = FastMCP("Search Server")

@mcp.tool
def web_search(query: str, max_results: int = 10, host: str = None) -> List[Dict[str, Any]]:
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
    if max_results > 25:
        max_results = 25
    elif max_results < 1:
        max_results = 1
    
    try:
        # Use default host if not provided
        if host is None:
            host = DEFAULT_SEARXNG_HOST
        # Call the existing search function
        results = search_general(query, host=host, max_results=max_results)
        
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
    except Exception as e:
        # Return an error result that the LLM can understand
        return [{"error": f"Search failed: {str(e)}"}]

@mcp.tool  
def search_summary(query: str, max_results: int = 5, host: str = None) -> Dict[str, Any]:
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
    if max_results > 15:
        max_results = 15
    elif max_results < 1:
        max_results = 1
    
    try:
        # Use default host if not provided
        if host is None:
            host = DEFAULT_SEARXNG_HOST
        # Call the existing search function
        results = search_general(query, host=host, max_results=max_results)
        
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
        
    except Exception as e:
        return {"error": f"Search failed: {str(e)}", "query": query}

if __name__ == "__main__":
    import sys
    
    # Check for HTTP mode flag
    if len(sys.argv) > 1 and sys.argv[1] == "--http":
        # Run with HTTP transport on port 3090
        mcp.run(transport="http", host="0.0.0.0", port=3090)
        print("Server running on http://localhost:3090")
    else:
        # Default stdio transport for MCP
        mcp.run()