# SearXNG MCP Server

A simple FastMCP server that exposes SearXNG search functionality as MCP tools for AI assistants.

## Tools

- **`search`** - Returns full search results with titles, URLs, snippets, scores
  - `query` (required) - search terms
  - `max_results` (optional) - number of results 
- **`fetch_content`** - Returns the content of a URL
  - `url` (required) - URL to fetch content from

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
./build.sh

# Run
docker-compose run -p 3090:3090 -e SEARXNG_HOST=http://localhost:8189 searxng-mcp
```
The server will be available at `http://localhost:3090/mcp`

NOTE! If you don't have an existing SearXNG instance, you can use the [setup-searxng-and-mcp-server.md](/doc/setup-searxng-and-mcp-server.md) doc. It has full instructions on setting up both SearXNG and the MCP server with Docker.

#### TODO
- [ ] Add support for setting search types (e.g. general, videos, news)
- [ ] Add support for setting search engines (e.g. google, bing, duckduckgo)
- [ ] Add instructions for simple python setup