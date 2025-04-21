from typing import List, Dict, Any
from .base_crawler import BaseCrawler

class NaukriCrawler(BaseCrawler):
    async def search(self, keywords: List[str], location: str) -> List[Dict[str, Any]]:
        try:
            # Create a new page with stealth settings
            async with self as crawler:
                page = await crawler.browser.new_page()
                
                # Navigate to Naukri
                await page.goto('https://www.naukri.com')
                
                # Fill search fields
                await page.fill('input[placeholder="Skills, Designations, Companies"]', ' '.join(keywords))
                await page.fill('input[placeholder="Enter location"]', location)
                await page.click('button[type="submit"]')
                
                # Wait for results
                await page.wait_for_selector('.jobTuple')
                
                # Extract job listings
                jobs = []
                job_cards = await page.query_selector_all('.jobTuple')
            
            for card in job_cards:
                job = {
                    'title': await card.query_selector('.title').inner_text(),
                    'company': await card.query_selector('.companyInfo').inner_text(),
                    'location': await card.query_selector('.location').inner_text(),
                    'url': await card.query_selector('a').get_attribute('href'),
                    'source': 'naukri'
                }
                jobs.append(job)
            
            return jobs
        except Exception as e:
            print(f"Error creating page: {e}")
            return []
        