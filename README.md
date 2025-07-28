# Searxng MCP Server

A simple FastMCP server that exposes SearxNG search functionality as MCP tools for AI assistants.

## Tools

- **`search`** - Returns full search results with titles, URLs, snippets, scores
  - `query` (required) - search terms
  - `max_results` (optional) - number of results 

## Setup

1. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2. **Ensure SearxNG is running** at `http://berry:8189` (or update the host in the code)

## Usage

**MCP mode (stdio):**
```bash
python -m src.server.mcp_server
```

**HTTP mode:**
```bash
python -m src.server.mcp_server --http
```
Server will run at `http://localhost:3090`

**With Docker (recommended):**

Build and run manually:
```bash
# Build the image
docker build -t searxng-mcp:latest .

# Run directly
docker run -p 3090:3090 -e SEARXNG_HOST=http://your-searxng-host:8189 searxng-mcp:latest

# Or using docker-compose (recommended)
docker-compose up -d
```

The server will be available at `http://localhost:3090`

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

