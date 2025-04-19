from abc import ABC, abstractmethod
from typing import List, Dict, Any
from playwright.async_api import async_playwright

class BaseCrawler(ABC):
    def __init__(self):
        self.playwright = None
        self.browser = None
        
    async def __aenter__(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.browser.close()
        await self.playwright.stop()

    @abstractmethod
    async def search(self, keywords: List[str], location: str) -> List[Dict[str, Any]]:
        pass