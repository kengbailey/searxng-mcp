# Searxng MCP Server

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
python -m src.server.mcp_server
```

**HTTP mode:**
```bash
python -m src.server.mcp_server --http
```
Server will run at `http://localhost:3090`

### Test it:

**Integration test:**
```bash
python -m tests.integration.test_client
```

**Unit tests:**
```bash
python -m unittest discover tests
```

**Functionality test:**
```bash
python test_functionality.py
```

### Use with Claude Desktop:

Add to your MCP config (`~/Library/Application Support/Claude/claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "search-server": {
      "command": "python",
      "args": ["-m", "src.server.mcp_server"],
      "cwd": "/absolute/path/to/searxng-mcp-server"
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