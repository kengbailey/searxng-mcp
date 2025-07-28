"""
Test script to demonstrate that the original functionality still works
after the refactoring
"""

# Test the refactored search functionality
from src.core.search import search_general, search_videos
from src.core.models import GeneralSearchResult, VideoSearchResult

def test_general_search():
    """Test general search functionality."""
    print("=== GENERAL SEARCH (Refactored) ===")
    try:
        general_results = search_general("apache iceberg latest features", max_results=5)
        print(f"Found {len(general_results)} results\n")
        
        for idx, result in enumerate(general_results, 1):
            print(f"Result {idx}:")
            print(f"  Title: {result.title}")
            print(f"  URL: {result.url}")
            print(f"  Score: {result.score}")
            print(f"  Category: {result.category}")
            if result.content:
                print(f"  Content: {result.content[:100]}...")
            else:
                print(f"  Content: None")
            print(f"  Author: {result.author}\n")
    except Exception as e:
        print(f"Error in general search: {e}")

def test_video_search():
    """Test video search functionality."""
    print("=== VIDEO SEARCH (Refactored) ===")
    try:
        video_results = search_videos("latest mkbhd review", max_results=5)
        print(f"Found {len(video_results)} video results\n")
        
        for idx, result in enumerate(video_results, 1):
            print(f"Video {idx}:")
            print(f"  Title: {result.title}")
            print(f"  URL: {result.url}")
            print(f"  Author: {result.author}")
            print(f"  Duration: {result.duration}")
            print(f"  Published: {result.published_date}")
            if result.content:
                print(f"  Summary: {result.content[:100]}...")
            else:
                print(f"  Summary: None")
            print(f"  Thumbnail: {result.thumbnail}\n")
    except Exception as e:
        print(f"Error in video search: {e}")

if __name__ == "__main__":
    test_general_search()
    print("\n" + "="*60 + "\n")
    test_video_search()