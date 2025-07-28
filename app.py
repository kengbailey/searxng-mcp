import os
import requests
from typing import List, Optional, Union
from pydantic import BaseModel

# Configuration
DEFAULT_SEARXNG_HOST = os.getenv('SEARXNG_HOST', 'http://berry:8189')

# Specific data models for different search types
class GeneralSearchResult(BaseModel):
    title: str
    url: str
    content: Optional[str] = None
    score: Optional[float] = None
    category: Optional[str] = None
    author: Optional[str] = None

class VideoSearchResult(BaseModel):
    title: str
    url: str
    content: Optional[str] = None
    published_date: Optional[str] = None
    duration: Optional[Union[str, float]] = None
    author: Optional[str] = None
    thumbnail: Optional[str] = None

# Raw response model for internal use
class RawResult(BaseModel):
    url: str
    title: str
    content: Optional[str] = None
    thumbnail: Optional[str] = None
    engine: str
    template: Optional[str] = None
    parsed_url: Optional[List[str]] = None
    img_src: Optional[str] = None
    priority: Optional[str] = None
    engines: Optional[List[str]] = None
    positions: Optional[List[int]] = None
    score: Optional[float] = None
    category: Optional[str] = None
    publishedDate: Optional[str] = None
    iframe_src: Optional[str] = None
    length: Optional[Union[str, float]] = None
    duration: Optional[Union[str, float]] = None
    author: Optional[str] = None

class RawSearxngResponse(BaseModel):
    query: str
    number_of_results: int
    results: List[RawResult]
    answers: List[dict] = []
    corrections: List[str] = []
    infoboxes: List[dict] = []
    suggestions: List[str] = []
    unresponsive_engines: List[List[str]] = []

# Internal function for making raw SearxNG requests
def _search_searxng_raw(query: str, host: str = None, engines=None, categories=None, max_results=None) -> RawSearxngResponse:
    """Internal function to perform raw SearxNG search."""
    if host is None:
        host = DEFAULT_SEARXNG_HOST
    url = f"{host}/search"
    params = {'q': query, 'format': 'json'}
    
    if engines:
        if isinstance(engines, list):
            params['engines'] = ','.join(engines)
        else:
            params['engines'] = engines
    if categories:
        if isinstance(categories, list):
            params['categories'] = ','.join(categories)
        else:
            params['categories'] = categories
            
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Slice results if max_results is specified
        if max_results is not None and 'results' in data:
            data['results'] = data['results'][:max_results]
        
        return RawSearxngResponse(**data)
    except requests.exceptions.RequestException as e:
        raise Exception(f"Search request failed: {e}")
    except Exception as e:
        raise Exception(f"Failed to parse search response: {e}")

def search_general(query: str, host: str = None, max_results: int = 15) -> List[GeneralSearchResult]:
    """
    Perform a general web search and return cleaned results.
    
    Args:
        query: The search query
        host: SearxNG server URL
        max_results: Maximum number of results to return
        
    Returns:
        List of GeneralSearchResult objects
    """
    raw_response = _search_searxng_raw(query, host, max_results=max_results)
    
    results = []
    for result in raw_response.results:
        results.append(GeneralSearchResult(
            title=result.title,
            url=result.url,
            content=result.content,
            score=result.score,
            category=result.category,
            author=result.author
        ))
    
    return results

def search_videos(query: str, host: str = None, engines: str = 'youtube', max_results: int = 10) -> List[VideoSearchResult]:
    """
    Perform a video search and return cleaned results.
    
    Args:
        query: The search query
        host: SearxNG server URL
        engines: Video engines to use (default: 'youtube')
        max_results: Maximum number of results to return
        
    Returns:
        List of VideoSearchResult objects
    """
    raw_response = _search_searxng_raw(
        query, 
        host, 
        engines=engines, 
        categories='videos', 
        max_results=max_results
    )
    
    results = []
    for result in raw_response.results:
        # Use length or duration, whichever is available
        duration = result.length or result.duration
        
        results.append(VideoSearchResult(
            title=result.title,
            url=result.url,
            content=result.content,
            published_date=result.publishedDate,
            duration=duration,
            author=result.author,
            thumbnail=result.img_src or result.thumbnail
        ))
    
    return results

# Example Usage
if __name__ == "__main__":
    # General search example
    print("=== GENERAL SEARCH ===")
    general_results = search_general("apache iceberg latest features", max_results=5)
    print(f"Found {len(general_results)} results\n")
    
    for idx, result in enumerate(general_results, 1):
        print(f"Result {idx}:")
        print(f"  Title: {result.title}")
        print(f"  URL: {result.url}")
        print(f"  Score: {result.score}")
        print(f"  Category: {result.category}")
        print(f"  Content: {result.content[:100]}..." if result.content else "  Content: None")
        print(f"  Author: {result.author}\n")

    # Video search example
    print("=== VIDEO SEARCH ===")
    video_results = search_videos("latest mkbhd review", max_results=5)
    print(f"Found {len(video_results)} video results\n")
    
    for idx, result in enumerate(video_results, 1):
        print(f"Video {idx}:")
        print(f"  Title: {result.title}")
        print(f"  URL: {result.url}")
        print(f"  Author: {result.author}")
        print(f"  Duration: {result.duration}")
        print(f"  Published: {result.published_date}")
        print(f"  Summary: {result.content[:100]}..." if result.content else "  Summary: None")
        print(f"  Thumbnail: {result.thumbnail}\n")