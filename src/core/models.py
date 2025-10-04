"""
Pydantic models for search results and API responses
"""

from typing import List, Optional, Union
from pydantic import BaseModel


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


# Output models for MCP tools
class SearchResultOutput(BaseModel):
    """Output model for general search results."""
    title: str
    url: str
    content: Optional[str] = None
    score: float


class VideoSearchResultOutput(BaseModel):
    """Output model for video search results."""
    url: str
    title: str
    author: Optional[str] = None
    content: Optional[str] = None
    length: Optional[Union[str, float]] = None


class FetchContentOutput(BaseModel):
    """Output model for fetch_content tool."""
    content: str
    content_length: int
    is_truncated: bool
    offset: int
    next_offset: Optional[int] = None
    total_length: int
    success: bool


class YouTubeContentOutput(BaseModel):
    """Output model for fetch_youtube_content tool."""
    video_id: str
    transcript: str
    transcript_length: int
    success: bool


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
