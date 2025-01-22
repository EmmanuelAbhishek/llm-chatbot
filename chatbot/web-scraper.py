import aiohttp
from bs4 import BeautifulSoup
import logging
from typing import Dict, Optional
from urllib.parse import urlparse
import json

logger = logging.getLogger(__name__)

class WebScraper:
    def __init__(self):
        self.allowed_domains = [
            'wikipedia.org',
            'educative.io',
            'developer.mozilla.org'
        ]
        self.session = None
    
    async def _get_session(self):
        """Get or create aiohttp session."""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session
    
    def _is_allowed_domain(self, url: str) -> bool:
        """Check if the domain is in the allowed list."""
        domain = urlparse(url).netloc
        return any(allowed in domain for allowed in self.allowed_domains)
    
    async def fetch_page(self, url: str) -> Optional[str]:
        """Fetch and parse webpage content."""
        if not self._is_allowed_domain(url):
            raise ValueError("Domain not in allowed list")
            
        try:
            session = await self._get_session()
            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Remove unwanted elements
                    for element in soup.find_all(['script', 'style', 'nav', 'footer']):
                        element.decompose()
                    
                    # Extract main content
                    main_content = soup.find('main') or soup.find('article') or soup.find('body')
                    
                    if main_content:
                        return main_content.get_text(separator=' ', strip=True)
                    return None
                    
        except Exception as e:
            logger.error(f"Error fetching webpage: {str(e)}")
            return None
    
    async def search_and_summarize(self, query: str) -> Dict[str, str]:
        """Search for relevant information and summarize it."""
        try:
            # Note: In a production environment, you would integrate with a search API
            # For now, we'll return a placeholder response
            return {
                'status': 'error',
                'message': 'Web search functionality requires search API integration'
            }
            
        except Exception as e:
            logger.error(f"Error in search and summarize: {str(e)}")
            return {
                'status': 'error',
                'message': 'Failed to search and summarize information'
            }

web_scraper = WebScraper()
