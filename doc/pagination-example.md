# Fetch Content Pagination Example

This document demonstrates how to use the `fetch_content` tool with pagination support.

## Basic Usage

### Single Request (Content < 30K characters)

```python
# Fetch content from a URL
result = fetch_content(url="https://example.com/article")

# Response structure:
{
    "content": "The full article text...",
    "content_length": 5432,
    "is_truncated": false,
    "offset": 0,
    "next_offset": null,
    "total_length": 5432,
    "success": true
}
```

## Pagination Usage

### Fetching Long Content (Content > 30K characters)

When content exceeds 30,000 characters, you'll need to make multiple requests:

```python
# Step 1: Fetch the first chunk
result1 = fetch_content(url="https://example.com/long-article")

# Response:
{
    "content": "First 30,000 characters...",
    "content_length": 30000,
    "is_truncated": true,
    "offset": 0,
    "next_offset": 30000,
    "total_length": 75000,
    "success": true
}

# Step 2: Check if truncated and fetch next chunk
if result1["is_truncated"]:
    result2 = fetch_content(
        url="https://example.com/long-article",
        offset=result1["next_offset"]  # Use next_offset from previous response
    )
    
    # Response:
    {
        "content": "Next 30,000 characters...",
        "content_length": 30000,
        "is_truncated": true,
        "offset": 30000,
        "next_offset": 60000,
        "total_length": 75000,
        "success": true
    }

# Step 3: Continue until is_truncated is false
if result2["is_truncated"]:
    result3 = fetch_content(
        url="https://example.com/long-article",
        offset=result2["next_offset"]
    )
    
    # Final chunk response:
    {
        "content": "Remaining 15,000 characters...",
        "content_length": 15000,
        "is_truncated": false,
        "offset": 60000,
        "next_offset": null,
        "total_length": 75000,
        "success": true
    }
```

## Complete Example: Fetching All Content

```python
def fetch_all_content(url: str) -> str:
    """Fetch all content from a URL, handling pagination automatically."""
    all_content = []
    offset = 0
    
    while True:
        result = fetch_content(url=url, offset=offset)
        
        if not result["success"]:
            raise Exception(f"Failed to fetch content: {result['error']}")
        
        all_content.append(result["content"])
        
        # Check if there's more content
        if not result["is_truncated"]:
            break
        
        # Use next_offset for the next request
        offset = result["next_offset"]
    
    return "".join(all_content)
```

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `content` | string | The content chunk (up to 30,000 characters) |
| `content_length` | int | Length of the returned content chunk |
| `is_truncated` | bool | `true` if more content is available, `false` if this is the last chunk |
| `offset` | int | The offset used for this request |
| `next_offset` | int/null | The offset to use for the next request (null if not truncated) |
| `total_length` | int | Total length of the full content |
| `success` | bool | `true` if fetch succeeded, `false` if an error occurred |

## Tips

1. **Always check `is_truncated`** to determine if you need to make additional requests
2. **Use `next_offset`** from the response for subsequent requests (don't calculate manually)
3. **Monitor `total_length`** to estimate total number of chunks needed
4. **Handle errors** by checking the `success` field before processing content
5. The chunk size (30,000 characters) is managed internally and not exposed to the API
