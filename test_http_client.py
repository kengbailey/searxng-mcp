"""
Test HTTP client for the FastMCP search server running in HTTP mode
"""

import asyncio
import aiohttp
import json

async def test_http_search():
    """Test the search server via HTTP"""
    
    base_url = "http://localhost:3090"
    
    async with aiohttp.ClientSession() as session:
        print("=== Testing FastMCP Search Server via HTTP ===\n")
        
        # Test 1: List available tools
        print("1. Available tools:")
        try:
            async with session.post(f"{base_url}/tools/list") as response:
                if response.status == 200:
                    data = await response.json()
                    tools = data.get('tools', [])
                    for tool in tools:
                        print(f"  - {tool.get('name')}: {tool.get('description', 'No description')}")
                else:
                    print(f"  Error: HTTP {response.status}")
        except Exception as e:
            print(f"  Error: {e}")
        
        print("\n" + "="*50 + "\n")
        
        # Test 2: Web search
        print("2. Testing web_search:")
        try:
            payload = {
                "name": "web_search",
                "arguments": {
                    "query": "FastMCP python",
                    "max_results": 3
                }
            }
            
            async with session.post(f"{base_url}/tools/call", 
                                   json=payload,
                                   headers={"Content-Type": "application/json"}) as response:
                if response.status == 200:
                    data = await response.json()
                    # Extract results from the response
                    if 'content' in data:
                        content = data['content']
                        if isinstance(content, list) and len(content) > 0:
                            results_text = content[0].get('text', '[]')
                            results = json.loads(results_text)
                            
                            print(f"Found {len(results)} results:")
                            for i, result in enumerate(results, 1):
                                print(f"  {i}. {result['title']}")
                                print(f"     URL: {result['url']}")
                                if result['content']:
                                    snippet = result['content'][:80] + "..."
                                    print(f"     Snippet: {snippet}")
                                print()
                        else:
                            print("  No content in response")
                    else:
                        print(f"  Unexpected response format: {data}")
                else:
                    print(f"  Error: HTTP {response.status}")
                    error_text = await response.text()
                    print(f"  Details: {error_text}")
        except Exception as e:
            print(f"  Error: {e}")
        
        print("\n" + "="*50 + "\n")
        
        # Test 3: Search summary
        print("3. Testing search_summary:")
        try:
            payload = {
                "name": "search_summary",
                "arguments": {
                    "query": "Python 2024 updates",
                    "max_results": 3
                }
            }
            
            async with session.post(f"{base_url}/tools/call", 
                                   json=payload,
                                   headers={"Content-Type": "application/json"}) as response:
                if response.status == 200:
                    data = await response.json()
                    if 'content' in data and data['content']:
                        summary_text = data['content'][0].get('text', '{}')
                        summary = json.loads(summary_text)
                        
                        if "error" not in summary:
                            print(f"Query: {summary['query']}")
                            print(f"Results found: {summary['total_results']}")
                            print("Top results:")
                            for result in summary['top_results']:
                                print(f"  {result['rank']}. {result['title']}")
                                print(f"     {result['url']}")
                                if result['snippet']:
                                    print(f"     {result['snippet'][:60]}...")
                                print()
                        else:
                            print(f"  Error: {summary['error']}")
                    else:
                        print(f"  Unexpected response: {data}")
                else:
                    print(f"  Error: HTTP {response.status}")
        except Exception as e:
            print(f"  Error: {e}")

if __name__ == "__main__":
    print("Make sure the server is running with: python search_mcp_server.py --http")
    print("Starting HTTP client test...\n")
    asyncio.run(test_http_search())