# SearXNG MCP Server

A simple FastMCP server that exposes SearXNG search functionality as MCP tools for AI assistants.

## Tools

- **`search`** - Returns full search results with titles, URLs, snippets, scores
  - `query` (required) - search terms
  - `max_results` (optional) - number of results (default: 10, max: 25)
- **`search_videos`** - Search for YouTube videos
  - `query` (required) - video search terms
  - `max_results` (optional) - number of results (default: 10, max: 20)
  - Returns: url, title, author, content summary, length
- **`fetch_content`** - Returns the content of a URL with pagination support
  - `url` (required) - URL to fetch content from
  - `offset` (optional) - starting position for content retrieval (default: 0)
  - **Pagination**: Content is retrieved in 30K character chunks. When truncated, use the `next_offset` value from the response to fetch the next chunk.

## Use with Docker
The below instructions will help you get setup with an HTTP MCP server. 

If you have an existing SearXNG instance, pull latest image and run manually
```bash
# Pull 
docker pull ghcr.io/kengbailey/searxng-mcp:latest

# Run 
docker run -p 3090:3090 -e SEARXNG_HOST=http://localhost:8189 ghcr.io/kengbailey/searxng-mcp:latest
```
Or you can build and run manually
```bash
# Build
docker build -t searxng-mcp .

# Run
docker run -p 3090:3090 -e SEARXNG_HOST=http://localhost:8189 searxng-mcp
```
The server will be available at `http://localhost:3090/mcp`

NOTE! If you don't have an existing SearXNG instance, you can use the [setup-searxng-and-mcp-server.md](/doc/setup-searxng-and-mcp-server.md) doc. It has full instructions on setting up both SearXNG and the MCP server with Docker.
