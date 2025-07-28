"""
Integration test client for the FastMCP search server
"""

import asyncio
from fastmcp import Client

async def test_search_tools():
    """Test the search tools exposed by the MCP server"""
    
    # Create a client that connects to the search server
    client = Client("src/server/mcp_server.py")
    
    async with client:
        print("=== Testing FastMCP Search Server ===\n")
        
        # Test 1: Basic web search
        print("1. Testing web_search tool:")
        try:
            response = await client.call_tool("web_search", {
                "query": "FastMCP python library",
                "max_results": 3
            })
            
            # Extract results from structured_content which contains the parsed data
            if hasattr(response, 'structured_content') and 'result' in response.structured_content:
                results = response.structured_content['result']
            else:
                # Fallback to parsing text content
                import json
                content = response.content[0].text if response.content else "[]"
                results = json.loads(content)
            
            print(f"Found {len(results)} results")
            for i, result in enumerate(results, 1):
                if "error" not in result:
                    print(f"  {i}. {result['title']}")
                    print(f"     URL: {result['url']}")
                    print(f"     Category: {result['category']}")
                    if result['content']:
                        snippet = result['content'][:100] + "..." if len(result['content']) > 100 else result['content']
                        print(f"     Snippet: {snippet}")
                    print()
                else:
                    print(f"  Error: {result['error']}")
                
        except Exception as e:
            print(f"Error calling web_search: {e}")
            import traceback
            traceback.print_exc()
        
        print("\n" + "="*50 + "\n")
        
        # Test 2: Search summary
        print("2. Testing search_summary tool:")
        try:
            response = await client.call_tool("search_summary", {
                "query": "latest Python developments 2024",
                "max_results": 5
            })
            
            # Extract summary from structured_content
            if hasattr(response, 'structured_content') and 'result' in response.structured_content:
                summary = response.structured_content['result']
            else:
                # Fallback to parsing text content
                import json
                content = response.content[0].text if response.content else "{}"
                summary = json.loads(content)
            
            if "error" not in summary:
                print(f"Query: {summary['query']}")
                print(f"Total results found: {summary['total_results']}")
                print("\nTop results:")
                for result in summary['top_results']:
                    print(f"  {result['rank']}. {result['title']}")
                    print(f"     URL: {result['url']}")
                    if result['snippet']:
                        print(f"     Snippet: {result['snippet']}")
                    print()
            else:
                print(f"Error: {summary['error']}")
                
        except Exception as e:
            print(f"Error calling search_summary: {e}")
            import traceback
            traceback.print_exc()

        print("\n" + "="*50 + "\n")
        
        # Test 3: List available tools
        print("3. Available tools in the server:")
        try:
            tools = await client.list_tools()
            for tool in tools:
                print(f"  - {tool.name}: {tool.description}")
        except Exception as e:
            print(f"Error listing tools: {e}")


if __name__ == "__main__":
    asyncio.run(test_search_tools())