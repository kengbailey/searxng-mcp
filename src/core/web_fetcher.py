"""
Web content fetching functionality
"""

import httpx
from bs4 import BeautifulSoup
import re
from typing import Optional
from .config import SearchConfig, SearchException


class WebContentFetcher:
    """Handles fetching and parsing web content."""
    
    def __init__(self):
        self.headers = {
            "User-Agent": SearchConfig.USER_AGENT
        }
    
    async def fetch_and_parse(self, url: str) -> tuple[str, bool]:
        """
        Fetch and parse content from a webpage.
        
        Args:
            url: The webpage URL to fetch content from
            
        Returns:
            Parsed text content from the webpage
            
        Raises:
            SearchException: If fetching or parsing fails
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url,
                    headers=self.headers,
                    follow_redirects=True,
                    timeout=SearchConfig.FETCH_TIMEOUT,
                )
                response.raise_for_status()
                
                # Parse the HTML
                try:
                    soup = BeautifulSoup(response.text, "lxml")
                except Exception as e:
                    # Fallback to html.parser if lxml fails
                    soup = BeautifulSoup(response.text, "html.parser")
                
                # Remove script and style elements
                unwanted_tags = [
                    "script", "style", "nav", "header", "footer", "aside", 
                    "advertisement", "ads", "sidebar", "menu", "widget", "banner"
                ]
                for element in soup(unwanted_tags):
                    element.decompose()
                
                # Get the text content
                text = soup.get_text()
                
                # Clean up the text
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split(" "))
                text = " ".join(chunk for chunk in chunks if chunk)
                
                # Remove extra whitespace
                text = re.sub(r"\s+", " ", text).strip()
                
                # Truncate if too long
                is_truncated = False
                if len(text) > SearchConfig.MAX_CONTENT_LENGTH:
                    text = text[:SearchConfig.MAX_CONTENT_LENGTH] + "... [content truncated]"
                    is_truncated = True
                
                return text, is_truncated
                
        except httpx.TimeoutException:
            raise SearchException("Request timed out while fetching the webpage")
            
        except httpx.HTTPError as e:
            raise SearchException(f"Could not access the webpage: {str(e)}")
            
        except Exception as e:
            raise SearchException(f"Unexpected error while fetching webpage: {str(e)}")