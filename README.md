# Searxng MCP Server

A simple FastMCP server that exposes SearxNG search functionality as MCP tools for AI assistants.

## Tools

- **`search`** - Returns full search results with titles, URLs, snippets, scores
  - `query` (required) - search terms
  - `max_results` (optional) - number of results 
- **`fetch_content`** - Returns the content of a URL
  - `url` (required) - URL to fetch content from

## Setup

1. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2. **Ensure SearxNG is running** at `http://localhost:8189` (or update the host in the code)

## Usage

**MCP mode (stdio):**
```bash
python -m src.server.mcp_server -sse
```
Server will run at `http://localhost:3090/sse`

**HTTP mode:**
```bash
python -m src.server.mcp_server --http
```
Server will run at `http://localhost:3090/mcp`

### Use with Docker

If you have an existing SearxNG instance, pull latest image and run manually
```bash
# Build the image
docker pull ghcr.io/kengbailey/searxng-mcp:latest

# Run directly
docker run -p 3090:3090 -e SEARXNG_HOST=http://localhost:8189 ghcr.io/kengbailey/searxng-mcp:latest
```
Or you can build and run manually
```bash
./build.sh

# Or using docker-compose (recommended)
# Be sure to edit docker compose w/ your Searxng host 
docker-compose up -d
```

The server will be available at `http://localhost:3090`

NOTE! If you don't have an existing SearxNG instance: [setup-searxng-and-mcp-server.md](/doc/setup-searxng-and-mcp-server.md)

### Use with Claude Desktop:

```json
{
  "mcpServers": {
    "search-server": {
      "command": "python",
      "args": ["-m", "src.server.mcp_server"],
      "cwd": "/absolute/path/to/searxng-mcp"
    }
  }
}
```

