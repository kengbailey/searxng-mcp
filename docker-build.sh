#!/bin/bash

# Simple Docker build and run script for the search MCP server

set -e

echo "Building Docker image for search-mcp-server..."
docker build -t search-mcp-server:latest .

echo "Build complete!"
echo ""
echo "To run the container:"
echo "  docker run -p 3090:3090 search-mcp-server:latest"
echo ""
echo "Or use docker-compose:"
echo "  docker-compose up -d"
echo ""
echo "The server will be available at http://localhost:3090"