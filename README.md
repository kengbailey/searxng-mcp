# FastMCP Search Server

A simple FastMCP server that exposes SearxNG search functionality as MCP tools for AI assistants.

## Setup

1. **Install dependencies:**
   ```bash
   pip install fastmcp requests pydantic
   ```

2. **Ensure SearxNG is running** at `http://berry:8189` (or update the host in the code)

## Usage

### Run the server:

**MCP mode (stdio):**
```bash
python search_mcp_server.py
```

**HTTP mode:**
```bash
python search_mcp_server.py --http
```
Server will run at `http://localhost:3090`

### Test it:

**MCP client:**
```bash
python test_search_client.py
```

**HTTP client:**
```bash
python test_http_client.py
```

### Use with Claude Desktop:

Add to your MCP config (`~/Library/Application Support/Claude/claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "search-server": {
      "command": "python",
      "args": ["/absolute/path/to/search_mcp_server.py"]
    }
  }
}
```

## Tools

- **`web_search`** - Returns full search results with titles, URLs, snippets, scores
- **`search_summary`** - Returns condensed results with top matches

Both tools accept:
- `query` (required) - search terms
- `max_results` (optional) - number of results 
- `host` (optional) - SearxNG server URL

## Files

- `search_mcp_server.py` - The MCP server
- `app.py` - SearxNG integration
- `test_search_client.py` - Test client