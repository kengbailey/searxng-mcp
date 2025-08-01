# Searxng MCP Server

A simple FastMCP server that exposes SearxNG search functionality as MCP tools for AI assistants.

## Tools

- **`search`** - Returns full search results with titles, URLs, snippets, scores
  - `query` (required) - search terms
  - `max_results` (optional) - number of results 
- **`fetch_content`** - Returns the content of a URL
  - `url` (required) - URL to fetch content from

## Use with Docker

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
docker-compose run -e SEARXNG_HOST=http://your-host:8080 searxng-mcp
```
The server will be available at `http://localhost:3090`

NOTE! If you don't have an existing SearxNG instance, you can use the [setup-searxng-and-mcp-server.md](/doc/setup-searxng-and-mcp-server.md) doc. It has full instructions on setting up both SearxNG and the MCP server with Docker.

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

