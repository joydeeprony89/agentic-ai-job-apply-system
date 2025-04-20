from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import random
import asyncio
from datetime import datetime
from urllib.parse import urlparse
from playwright.async_api import async_playwright, Browser, Page, TimeoutError

from core.config import settings
from .rate_limiter import rate_limiter


class BaseCrawler(ABC):
    """
    Base crawler class for job sites.
    """
    def __init__(self, domain: str = None, user_agent: str = None):
        self.playwright = None
        self.browser = None
        self.domain = domain
        self.user_agent = user_agent or self._get_random_user_agent()
        self.success_count = 0
        self.error_count = 0
        self.last_crawl_time = None
        
    async def __aenter__(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-dev-shm-usage',
            ]
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    @abstractmethod
    async def search(self, keywords: List[str], location: str) -> List[Dict[str, Any]]:
        """
        Search for jobs with the given keywords and location.
        
        Args:
            keywords: List of search keywords
            location: Job location
            
        Returns:
            List of job dictionaries
        """
        pass
    
    async def _create_page(self) -> Page:
        """
        Create a new page with stealth settings.
        
        Returns:
            Configured browser page
        """
        context = await self.browser.new_context(
            user_agent=self.user_agent,
            viewport={'width': 1920, 'height': 1080},
            device_scale_factor=1,
        )
        
        # Add stealth settings
        await context.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => false,
        });
        """)
        
        page = await context.new_page()
        
        # Set default timeout
        page.set_default_timeout(30000)
        
        return page
    
    async def _navigate(self, page: Page, url: str) -> bool:
        """
        Navigate to a URL with rate limiting.
        
        Args:
            page: Browser page
            url: URL to navigate to
            
        Returns:
            True if navigation was successful
        """
        domain = urlparse(url).netloc
        
        # Apply rate limiting
        await rate_limiter.wait(domain or self.domain)
        
        try:
            response = await page.goto(url, wait_until='domcontentloaded')
            
            # Check for successful navigation
            if response and response.ok:
                rate_limiter.record_success(domain or self.domain)
                return True
            else:
                status = response.status if response else 0
                rate_limiter.record_failure(domain or self.domain, status)
                return False
                
        except Exception as e:
            rate_limiter.record_failure(domain or self.domain)
            print(f"Navigation error: {e}")
            return False
    
    async def _random_delay(self, min_seconds: float = 1.0, max_seconds: float = 3.0) -> None:
        """
        Wait for a random amount of time to simulate human behavior.
        
        Args:
            min_seconds: Minimum wait time in seconds
            max_seconds: Maximum wait time in seconds
        """
        delay = random.uniform(min_seconds, max_seconds)
        await asyncio.sleep(delay)
    
    def _get_random_user_agent(self) -> str:
        """
        Get a random user agent string.
        
        Returns:
            Random user agent string
        """
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        ]
        return random.choice(user_agents)
    
    def update_stats(self, success: bool) -> None:
        """
        Update crawler statistics.
        
        Args:
            success: Whether the crawl was successful
        """
        self.last_crawl_time = datetime.now()
        if success:
            self.success_count += 1
        else:
            self.error_count += 1