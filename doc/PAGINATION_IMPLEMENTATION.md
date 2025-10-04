# Pagination Implementation Summary

## Overview
Added pagination support to the `fetch_content` tool using an offset-based approach, allowing retrieval of content that exceeds the 30,000 character limit.

## Implementation Approach
**Selected Option:** Pagination with offset parameter (Option #2 from planning phase)

### Why This Approach?
- Simple and intuitive for AI models to understand
- Stateless design (no server-side session management)
- Backward compatible (offset defaults to 0)
- Standard pagination pattern familiar to developers
- Chunk size kept internal (30K chars) - not exposed to API users

## Changes Made

### 1. Core Web Fetcher (`src/core/web_fetcher.py`)
- **Updated `fetch_and_parse` signature:**
  - Added `offset: int = 0` parameter
  - Changed return type to `tuple[str, bool, int, int]` (content, is_truncated, next_offset, total_length)
  
- **Added `_apply_offset_and_chunk` helper method:**
  - Applies offset to full content
  - Chunks content into 30K character segments
  - Calculates next_offset and truncation status
  - Handles edge cases (offset beyond content, negative offset)

### 2. Handler (`src/server/handlers.py`)
- **Updated `fetch_content` method:**
  - Added `offset: int = 0` parameter
  - Enhanced response structure with pagination metadata:
    - `offset`: Current offset used
    - `next_offset`: Offset for next request (null if complete)
    - `total_length`: Total content length

### 3. MCP Tool Definition (`src/server/mcp_server.py`)
- Added `offset` parameter to tool signature
- Enhanced docstring with detailed pagination instructions
- Documented response fields

### 4. Tests (`tests/test_fetch.py`)
- Updated all existing tests for new signature
- Added comprehensive pagination tests:
  - `test_pagination_with_offset`: Tests multi-chunk fetching
  - `test_offset_beyond_content`: Tests offset validation
  - `test_negative_offset`: Tests negative offset handling
  - `test_small_content_no_truncation`: Tests non-truncated content
- All 9 tests passing

### 5. Documentation
- Updated README.md with pagination feature description
- Created `doc/pagination-example.md` with usage examples
- Created this implementation summary

## API Changes

### Request
```python
fetch_content(url: str, offset: int = 0)
```

### Response Structure
```json
{
    "content": "chunk of text...",
    "content_length": 30000,
    "is_truncated": true,
    "offset": 0,
    "next_offset": 30000,
    "total_length": 75000,
    "success": true
}
```

## Usage Pattern

```python
# Fetch first chunk
result = fetch_content(url="https://example.com/article")

# Continue fetching if truncated
while result["is_truncated"]:
    result = fetch_content(
        url="https://example.com/article",
        offset=result["next_offset"]
    )
```

## Key Features

1. **Backward Compatible:** Existing calls without offset work unchanged
2. **Stateless:** No server-side state management needed
3. **Predictable:** Chunk size is consistent (30K chars)
4. **Edge Case Handling:**
   - Negative offsets treated as 0
   - Offsets beyond content return empty string
   - Small content (< 30K) never truncated

## Testing Results
```
================================ test session starts ================================
tests/test_fetch.py::TestWebContentFetcher::test_fetch_valid_url PASSED       [ 11%]
tests/test_fetch.py::TestWebContentFetcher::test_fetch_invalid_url PASSED     [ 22%]
tests/test_fetch.py::TestWebContentFetcher::test_content_truncation PASSED    [ 33%]
tests/test_fetch.py::TestWebContentFetcher::test_content_cleaning PASSED      [ 44%]
tests/test_fetch.py::TestWebContentFetcher::test_fetch_pdf_content PASSED     [ 55%]
tests/test_fetch.py::TestWebContentFetcher::test_pagination_with_offset PASSED [ 66%]
tests/test_fetch.py::TestWebContentFetcher::test_offset_beyond_content PASSED [ 77%]
tests/test_fetch.py::TestWebContentFetcher::test_negative_offset PASSED       [ 88%]
tests/test_fetch.py::TestWebContentFetcher::test_small_content_no_truncation PASSED [100%]

=========================== 9 passed in 5.69s ===========================
```

## Trade-offs

### Pros
- Simple to implement and use
- No server-side state required
- Clear and predictable behavior
- Easy for AI models to chain requests

### Cons
- Re-fetches full content on each request (not cached)
- Multiple network requests for very long content
- Client must track offset between requests

## Future Enhancements (Optional)
- Add optional caching for recently fetched content
- Support custom chunk sizes (while maintaining default)
- Add content compression for large responses
- Implement streaming support for real-time content delivery
