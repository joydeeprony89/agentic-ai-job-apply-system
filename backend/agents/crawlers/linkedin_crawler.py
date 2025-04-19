from typing import List, Dict, Any
from .base_crawler import BaseCrawler

class LinkedInCrawler(BaseCrawler):
    async def search(self, keywords: List[str], location: str) -> List[Dict[str, Any]]:
        async with self as crawler:
            page = await crawler.browser.new_page()
            
            # Navigate to LinkedIn jobs
            await page.goto('https://www.linkedin.com/jobs')
            
            # Fill search fields
            await page.fill('input[aria-label="Search job titles or companies"]', ' '.join(keywords))
            await page.fill('input[aria-label="City, state, or zip code"]', location)
            await page.click('button[type="submit"]')
            
            # Wait for results
            await page.wait_for_selector('.job-card-container')
            
            # Extract job listings
            jobs = []
            job_cards = await page.query_selector_all('.job-card-container')
            
            for card in job_cards:
                job = {
                    'title': await card.query_selector('.job-card-list__title').inner_text(),
                    'company': await card.query_selector('.job-card-container__company-name').inner_text(),
                    'location': await card.query_selector('.job-card-container__metadata-item').inner_text(),
                    'url': await card.query_selector('a').get_attribute('href'),
                    'source': 'linkedin'
                }
                jobs.append(job)
            
            return jobs