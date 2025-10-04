# YouTube Transcript Implementation

## Overview
Added `fetch_youtube_content` tool to transcribe YouTube videos using yt-dlp and a Speech-to-Text (STT) service.

## Implementation Details

### New Files Created
1. **`src/core/youtube_fetcher.py`**
   - Core functionality for downloading YouTube audio and transcribing
   - Uses yt-dlp to download smallest audio format (opus)
   - Integrates with OpenAI-compatible STT endpoint
   - Automatic cleanup of temporary files

2. **`tests/test_youtube_content.py`**
   - Comprehensive test suite (6 tests)
   - Tests video ID extraction, downloading, transcription
   - Tests error handling and cleanup

### Modified Files

1. **`src/core/config.py`**
   - Added STT configuration:
     - `STT_ENDPOINT` - STT service URL (default: `http://192.168.8.116:8000/v1`)
     - `STT_MODEL` - Model name (default: `Systran/faster-distil-whisper-large-v3`)
     - `STT_API_KEY` - API key (default: `dummy`)

2. **`src/core/models.py`**
   - Added `YouTubeContentOutput` model with:
     - `video_id` - Extracted YouTube video ID
     - `transcript` - Full transcription text
     - `transcript_length` - Character count
     - `success` - Boolean status

3. **`src/server/handlers.py`**
   - Added `fetch_youtube_content` handler
   - Validates input and handles errors
   - Returns structured output

4. **`src/server/mcp_server.py`**
   - Exposed new `fetch_youtube_content` tool
   - Accepts video ID or full YouTube URL
   - Includes proper documentation and annotations

5. **`docker-compose.yml`**
   - Added environment variables:
     - `STT_ENDPOINT`
     - `STT_MODEL`
     - `STT_API_KEY`

6. **`requirements.txt`**
   - Added `yt-dlp==2024.12.23`
   - Added `openai==1.59.5`

7. **`README.md`**
   - Documented new tool with usage details

## Usage

### Input
```python
fetch_youtube_content(video_id="dQw4w9WgXcQ")
# or
fetch_youtube_content(video_id="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
```

### Output
```json
{
  "video_id": "dQw4w9WgXcQ",
  "transcript": "Full transcribed text here...",
  "transcript_length": 1234,
  "success": true
}
```

## Configuration

The tool requires a running STT service. Configure via environment variables:

```bash
STT_ENDPOINT=http://192.168.8.116:8000/v1
STT_MODEL=Systran/faster-distil-whisper-large-v3
STT_API_KEY=dummy
```

## Testing

All tests pass (31 total):
- 6 new YouTube content tests
- 25 existing tests remain passing

```bash
pytest tests/test_youtube_content.py -v  # Run YouTube tests
pytest tests/ -v                          # Run all tests
```

## Features

- **Flexible Input**: Accepts both video IDs and full YouTube URLs
- **Efficient**: Downloads only audio in smallest format (opus)
- **Automatic Cleanup**: Temporary files are always deleted
- **Error Handling**: Comprehensive error handling with meaningful messages
- **OpenAI Compatible**: Works with any OpenAI-compatible STT endpoint
