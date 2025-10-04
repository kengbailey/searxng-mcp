"""
Integration tests for YouTube content fetching
These tests make real network calls and should be run separately from unit tests
"""

import os
import pytest
from src.core.youtube_fetcher import YouTubeContentFetcher
from src.core.config import SearchException


class TestYouTubeIntegration:
    """Integration test suite for real YouTube operations."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.fetcher = YouTubeContentFetcher()
    
    @pytest.mark.integration
    def test_video_id_extraction_from_various_formats(self):
        """
        Test video ID extraction from various YouTube URL formats.
        This test can run anywhere as it only tests URL parsing.
        """
        test_cases = [
            # (input, expected_video_id)
            ("https://www.youtube.com/watch?v=1x2nv67NQVc", "1x2nv67NQVc"),
            ("https://youtu.be/1x2nv67NQVc", "1x2nv67NQVc"),
            ("1x2nv67NQVc", "1x2nv67NQVc"),  # Already a video ID
        ]
        
        for input_url, expected_id in test_cases:
            result = self.fetcher._extract_video_id(input_url)
            assert result == expected_id, f"Failed to extract ID from: {input_url}"
            print(f"✅ Extracted '{expected_id}' from '{input_url}'")
    
    @pytest.mark.integration
    def test_invalid_video_id_extraction(self):
        """Test that invalid URLs raise appropriate exceptions."""
        invalid_inputs = [
            "https://invalid-url.com",
            "not-a-url-at-all",
        ]
        
        for invalid_input in invalid_inputs:
            with pytest.raises(SearchException) as exc_info:
                self.fetcher._extract_video_id(invalid_input)
            assert "Failed to extract video ID" in str(exc_info.value)
            print(f"✅ Correctly rejected invalid input: {invalid_input}")
    
    @pytest.mark.integration
    def test_full_fetch_and_transcribe_pipeline(self):
        """
        Full end-to-end test: download YouTube video and transcribe.
        
        This test now works both inside and outside Docker!
        
        REQUIREMENTS:
        - STT service must be available and configured
        - Network access to download YouTube video
        """
        video_url = "https://www.youtube.com/watch?v=1x2nv67NQVc"
        
        print(f"\n🎬 Testing full pipeline with: {video_url}")
        
        # Execute the full fetch and transcribe operation
        video_id, transcript = self.fetcher.fetch_and_transcribe(video_url)
        
        # Verify video ID was extracted correctly
        assert video_id == "1x2nv67NQVc", f"Expected '1x2nv67NQVc' but got '{video_id}'"
        
        # Verify transcript was generated
        assert isinstance(transcript, str), "Transcript should be a string"
        assert len(transcript) > 100, f"Transcript too short ({len(transcript)} chars), likely failed"
        
        # Success output
        print(f"\n✅ Successfully completed full pipeline:")
        print(f"   Video ID: {video_id}")
        print(f"   Transcript length: {len(transcript)} characters")
        print(f"   First 150 chars: {transcript[:150]}...")


if __name__ == "__main__":
    # Allow running this test file directly
    pytest.main([__file__, "-v", "-m", "integration", "-s"])
