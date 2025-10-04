## How to setup SearxNG and the MCP server using docker 

1. Create a directory for your SearxNG data:
```bash
mkdir searxng-data
```
2. Create a [searxng-compose.yml](/doc/searxng-compose.yml) for Searxng. 
- Be sure to update the volume to your local directory. 
```yaml
services:
  searxng:
    container_name: searxng
    image: docker.io/searxng/searxng:latest
    restart: unless-stopped
    ports:
      - "8189:8080"
    volumes:
      - ./searxng-data:/etc/searxng:rw
```

3. Run Searxng compose
```bash 
docker compose -f searxng-compose.yml up -d
```

4. Stop Searxng container and update settings 
```bash
docker compose -f searxng-compose.yml down
```
- First run will create a settings.yaml file in the searxng-data directory. 
- Update the [settings.yaml](/doc/settings.yml) in new directory to look like this
```yaml
use_default_settings: true

server:
  bind_address: "0.0.0.0"
  secret_key: "mySecretKey"  # Generate a random key
  port: 8080

search:
  safe_search: 0
  formats:
    - html
    - json     # Enables API searches

engines:
  - name: google
    engine: google
    shortcut: g

  - name: duckduckgo
    engine: duckduckgo
    shortcut: d

  - name: bing
    engine: bing
    shortcut: b

server.limiter: false
```

5. Start your Searxng container again after updating the file
```bash
docker compose searxng-compose.yml up -d
```

6. Create and run the [webintel-mcp-compose.yml](/doc/searxng-mcp-compose.yaml) docker container
```yaml
services:
  webintel-mcp:
    image: ghcr.io/kengbailey/webintel-mcp:latest
    container_name: webintel-mcp
    ports:
      - "3090:3090"
    environment:
      - SEARXNG_HOST=http://localhost:8080
    restart: unless-stopped
```
```bash
docker compose webintel-mcp-compose.yml up -d
```
You should have a running SearXNG service and WebIntel MCP server
- SearXNG: http://localhost:8189/search
- WebIntel MCP: http://localhost:3090/mcp
