# YouTube Content Fetcher Bug Fix

## Issue
The `fetch_youtube_content` tool was failing with error: "The downloaded file is empty"

## Root Cause
File path mismatch between where yt-dlp saved the audio file and where the code was trying to read it:

1. Created temp file: `/tmp/xyz.opus`
2. Told yt-dlp to output to: `/tmp/xyz` (without extension)
3. yt-dlp's FFmpegExtractAudio created: `/tmp/xyz.opus`
4. Code tried to read the **original empty temp file** instead of yt-dlp's output

## Fix Applied

### 1. Changed File Handling Strategy
**Before:**
```python
with tempfile.NamedTemporaryFile(suffix='.opus', delete=False) as tmp:
    audio_path = Path(tmp.name)

ydl_opts = {
    'outtmpl': str(audio_path.with_suffix('')),  # Wrong path
    ...
}

with open(audio_path, 'rb') as f:  # Opens wrong file!
```

**After:**
```python
temp_dir = tempfile.mkdtemp()
audio_base = Path(temp_dir) / "audio"

ydl_opts = {
    'outtmpl': str(audio_base),  # Correct base path
    ...
}

audio_path = audio_base.with_suffix('.opus')  # Correct final path
```

### 2. Added File Validation
```python
# Verify file exists and has content
if not audio_path.exists():
    raise SearchException("Audio file was not created by yt-dlp")

if audio_path.stat().st_size == 0:
    raise SearchException("Downloaded audio file is empty")
```

### 3. Improved Cleanup
Changed from `Path.unlink()` to `shutil.rmtree()` to properly clean up the entire temporary directory.

## Testing

### Integration Test
Created `tests/test_youtube_integration.py` with real download test:
```bash
pytest tests/test_youtube_integration.py::TestYouTubeIntegration::test_download_real_video -v -s
```

**Result:** ✅ Successfully downloaded 3.3 MB audio file

### Unit Tests
Updated all unit tests to match new implementation:
- Changed mocks from `Path.unlink` to `shutil.rmtree`
- Added mocks for `Path.exists()` and `Path.stat()`
- All 6 unit tests passing

### Full Test Suite
All 31 tests pass (excluding integration tests by default)

## Files Modified
1. `src/core/youtube_fetcher.py` - Fixed file path handling
2. `tests/test_youtube_content.py` - Updated unit tests
3. `tests/test_youtube_integration.py` - New integration test
4. `pytest.ini` - Added test markers configuration

## Verification
To test with a real video:
```bash
# Run integration test
pytest -m integration tests/test_youtube_integration.py -v -s

# Or test directly via MCP tool
fetch_youtube_content(video_id="z0dw4z5em2s")
