# Docker Setup for Search MCP Server

This document explains how to build and run the Search MCP Server using Docker.

## Quick Start

### Using the build script
```bash
./docker-build.sh
docker run -p 3090:3090 search-mcp-server:latest
```

### Using Docker Compose (Recommended)
```bash
docker-compose up -d
```

### Manual Docker Commands
```bash
# Build the image
docker build -t search-mcp-server:latest .

# Run the container
docker run -p 3090:3090 -e SEARXNG_HOST=http://your-searxng-host:8189 search-mcp-server:latest
```

## Configuration

The application can be configured using environment variables:

- `SEARXNG_HOST`: URL of your SearxNG instance (default: `http://berry:8189`)

### Example with custom SearxNG host:
```bash
docker run -p 3090:3090 -e SEARXNG_HOST=http://localhost:8080 search-mcp-server:latest
```

## Docker Compose Configuration

The `docker-compose.yml` file includes:
- Port mapping: `3090:3090`
- Environment variable for SearxNG host
- Restart policy: `unless-stopped`
- Container name: `search-mcp-server`

## Usage

Once running, the server will be available at:
- **HTTP Mode**: `http://localhost:3090`
- **MCP Tools**: Available via the FastMCP interface

### Available endpoints:
- `web_search`: General web search functionality
- `search_summary`: Summarized search results

## Stopping the Container

### Docker Compose:
```bash
docker-compose down
```

### Docker run:
```bash
docker stop search-mcp-server
```

## Logs

### View logs:
```bash
# Docker Compose
docker-compose logs -f search-app

# Docker run
docker logs -f search-mcp-server
```

## Troubleshooting

1. **Port already in use**: Change the port mapping to `-p 3091:3090`
2. **SearxNG connection issues**: Verify the `SEARXNG_HOST` environment variable
3. **Build failures**: Ensure all files are present and Docker has sufficient resources

## Development

For development, you can mount the source code:
```bash
docker run -p 3090:3090 -v $(pwd):/app search-mcp-server:latest
```