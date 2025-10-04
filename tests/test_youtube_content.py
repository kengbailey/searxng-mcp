"""
Tests for YouTube content fetching functionality
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from src.core.youtube_fetcher import YouTubeContentFetcher
from src.core.config import SearchException


class TestYouTubeContentFetcher:
    """Test suite for YouTubeContentFetcher."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.fetcher = YouTubeContentFetcher()
    
    def test_extract_video_id_from_id(self):
        """Test extracting video ID when already provided as ID."""
        video_id = "dQw4w9WgXcQ"
        result = self.fetcher._extract_video_id(video_id)
        assert result == video_id
    
    @patch('yt_dlp.YoutubeDL')
    def test_extract_video_id_from_url(self, mock_ydl_class):
        """Test extracting video ID from YouTube URL."""
        mock_ydl = MagicMock()
        mock_ydl.extract_info.return_value = {'id': 'dQw4w9WgXcQ'}
        mock_ydl_class.return_value.__enter__.return_value = mock_ydl
        
        video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        result = self.fetcher._extract_video_id(video_url)
        
        assert result == "dQw4w9WgXcQ"
        mock_ydl.extract_info.assert_called_once_with(video_url, download=False)
    
    @patch('yt_dlp.YoutubeDL')
    def test_extract_video_id_failure(self, mock_ydl_class):
        """Test handling of video ID extraction failure."""
        mock_ydl = MagicMock()
        mock_ydl.extract_info.side_effect = Exception("Invalid URL")
        mock_ydl_class.return_value.__enter__.return_value = mock_ydl
        
        with pytest.raises(SearchException) as exc_info:
            self.fetcher._extract_video_id("https://invalid-url-that-will-fail")
        
        assert "Failed to extract video ID" in str(exc_info.value)
    
    @patch('pathlib.Path.rmdir')
    @patch('pathlib.Path.unlink')
    @patch('tempfile.mkdtemp')
    @patch('src.core.youtube_fetcher.OpenAI')
    @patch('yt_dlp.YoutubeDL')
    @patch('builtins.open', create=True)
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.stat')
    def test_fetch_and_transcribe_success(self, mock_stat, mock_exists, mock_open, mock_ydl_class, mock_openai_class, mock_mkdtemp, mock_unlink, mock_rmdir):
        """Test successful YouTube content fetching and transcription."""
        # Mock temp directory creation
        mock_mkdtemp.return_value = '/tmp/youtube_audio_test123'
        
        # Mock yt-dlp
        mock_ydl = MagicMock()
        mock_ydl_class.return_value.__enter__.return_value = mock_ydl
        
        # Mock file exists and has size
        mock_exists.return_value = True
        mock_stat.return_value.st_size = 1024
        
        # Mock OpenAI client
        mock_client = MagicMock()
        mock_transcription = MagicMock()
        mock_transcription.create.return_value = "This is a test transcript."
        mock_client.audio.transcriptions = mock_transcription
        mock_openai_class.return_value = mock_client
        
        # Mock file operations
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        
        video_id = "dQw4w9WgXcQ"
        result_id, transcript = self.fetcher.fetch_and_transcribe(video_id)
        
        assert result_id == video_id
        assert transcript == "This is a test transcript."
        mock_ydl.download.assert_called_once()
        mock_transcription.create.assert_called_once()
        mock_unlink.assert_called_once()
        mock_rmdir.assert_called_once()
    
    @patch('pathlib.Path.rmdir')
    @patch('pathlib.Path.unlink')
    @patch('pathlib.Path.exists')
    @patch('tempfile.mkdtemp')
    @patch('yt_dlp.YoutubeDL')
    def test_fetch_and_transcribe_download_failure(self, mock_ydl_class, mock_mkdtemp, mock_exists, mock_unlink, mock_rmdir):
        """Test handling of download failure."""
        # Mock temp directory creation
        mock_mkdtemp.return_value = '/tmp/youtube_audio_test123'
        
        mock_ydl = MagicMock()
        mock_ydl.download.side_effect = Exception("Download failed")
        mock_ydl_class.return_value.__enter__.return_value = mock_ydl
        
        # Mock that file and directory exist so cleanup is attempted
        mock_exists.return_value = True
        
        with pytest.raises(SearchException) as exc_info:
            self.fetcher.fetch_and_transcribe("dQw4w9WgXcQ")
        
        assert "Failed to fetch/transcribe YouTube content" in str(exc_info.value)
        # Cleanup should still be called
        mock_unlink.assert_called_once()
        mock_rmdir.assert_called_once()
    
    @patch('pathlib.Path.rmdir')
    @patch('pathlib.Path.unlink')
    @patch('tempfile.mkdtemp')
    @patch('src.core.youtube_fetcher.OpenAI')
    @patch('yt_dlp.YoutubeDL')
    @patch('builtins.open', create=True)
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.stat')
    def test_fetch_and_transcribe_stt_failure(self, mock_stat, mock_exists, mock_open, mock_ydl_class, mock_openai_class, mock_mkdtemp, mock_unlink, mock_rmdir):
        """Test handling of STT transcription failure."""
        # Mock temp directory creation
        mock_mkdtemp.return_value = '/tmp/youtube_audio_test123'
        
        # Mock yt-dlp success
        mock_ydl = MagicMock()
        mock_ydl_class.return_value.__enter__.return_value = mock_ydl
        
        # Mock file and directory exist and has size
        mock_exists.return_value = True
        mock_stat.return_value.st_size = 1024
        
        # Mock OpenAI client failure
        mock_client = MagicMock()
        mock_transcription = MagicMock()
        mock_transcription.create.side_effect = Exception("Transcription failed")
        mock_client.audio.transcriptions = mock_transcription
        mock_openai_class.return_value = mock_client
        
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        
        with pytest.raises(SearchException) as exc_info:
            self.fetcher.fetch_and_transcribe("dQw4w9WgXcQ")
        
        assert "Failed to fetch/transcribe YouTube content" in str(exc_info.value)
        # Cleanup should still be called
        mock_unlink.assert_called_once()
        mock_rmdir.assert_called_once()
