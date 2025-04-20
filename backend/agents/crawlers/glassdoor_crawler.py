"""
Glassdoor job crawler.
"""
from typing import List, Dict, Any, Optional
import re
from urllib.parse import quote
from datetime import datetime
from playwright.async_api import TimeoutError

from .base_crawler import BaseCrawler


class GlassdoorCrawler(BaseCrawler):
    """
    Glassdoor job crawler.
    """
    def __init__(self):
        super().__init__(domain="glassdoor.com")
        self.base_url = "https://www.glassdoor.com/Job/jobs.htm"
    
    async def search(self, keywords: List[str], location: str) -> List[Dict[str, Any]]:
        """
        Search for jobs on Glassdoor.
        
        Args:
            keywords: List of search keywords
            location: Job location
            
        Returns:
            List of job dictionaries
        """
        search_success = False
        jobs = []
        
        try:
            async with self as crawler:
                page = await self._create_page()
                
                # Construct search URL
                keyword_string = ' '.join(keywords)
                search_url = f"{self.base_url}?sc.keyword={quote(keyword_string)}&locT=C&locId=1147401&locKeyword={quote(location)}"
                
                # Navigate to Glassdoor jobs
                if not await self._navigate(page, search_url):
                    self.update_stats(False)
                    return []
                
                # Check for and handle login modal
                try:
                    close_button = await page.query_selector('button[alt="Close"], .modal_closeIcon')
                    if close_button:
                        await close_button.click()
                        await self._random_delay(1.0, 2.0)
                except Exception:
                    pass  # Ignore if no modal
                
                # Wait for results
                try:
                    await page.wait_for_selector('.react-job-listing, .jobCard', timeout=10000)
                except TimeoutError:
                    self.update_stats(False)
                    return []
                
                # Random delay to simulate human behavior
                await self._random_delay(2.0, 4.0)
                
                # Extract job listings
                job_cards = await page.query_selector_all('.react-job-listing, .jobCard')
                
                for card in job_cards:
                    try:
                        # Extract basic job info
                        title_elem = await card.query_selector('.job-title, .jobTitle')
                        company_elem = await card.query_selector('.employer-name, .jobEmployer')
                        location_elem = await card.query_selector('.location, .jobLocation')
                        
                        if not title_elem:
                            continue
                        
                        title = await title_elem.inner_text()
                        company = await company_elem.inner_text() if company_elem else "Unknown Company"
                        job_location = await location_elem.inner_text() if location_elem else location
                        
                        # Get the job link
                        url = await card.get_attribute('href') or await card.evaluate('el => el.querySelector("a").href')
                        
                        if not url:
                            continue
                        
                        # Try to extract salary if available
                        salary_elem = await card.query_selector('.salary-estimate, span:has-text("$")')
                        salary = await salary_elem.inner_text() if salary_elem else None
                        
                        # Basic job data
                        job = {
                            'title': title.strip(),
                            'company': company.strip(),
                            'location': job_location.strip(),
                            'url': url,
                            'source': 'glassdoor',
                            'search_date': datetime.now().isoformat(),
                            'salary': salary.strip() if salary else None,
                        }
                        
                        jobs.append(job)
                        
                        # Limit to 20 jobs per search to avoid overloading
                        if len(jobs) >= 20:
                            break
                    
                    except Exception as e:
                        print(f"Error extracting Glassdoor job card: {e}")
                        continue
                
                # Get job details for first 5 jobs
                detailed_jobs = []
                for job in jobs[:5]:
                    try:
                        job_details = await self._get_job_details(page, job['url'])
                        if job_details:
                            detailed_jobs.append({**job, **job_details})
                        else:
                            detailed_jobs.append(job)
                    except Exception as e:
                        print(f"Error getting Glassdoor job details: {e}")
                        detailed_jobs.append(job)
                
                search_success = True
                jobs = detailed_jobs + jobs[5:]  # Combine detailed and non-detailed jobs
        
        except Exception as e:
            print(f"Glassdoor crawler error: {e}")
            search_success = False
        
        # Update crawler stats
        self.update_stats(search_success)
        
        return jobs
    
    async def _get_job_details(self, page, job_url: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed job information.
        
        Args:
            page: Browser page
            job_url: URL of the job listing
            
        Returns:
            Dictionary with job details
        """
        if not await self._navigate(page, job_url):
            return None
        
        # Check for and handle login modal
        try:
            close_button = await page.query_selector('button[alt="Close"], .modal_closeIcon')
            if close_button:
                await close_button.click()
                await self._random_delay(1.0, 2.0)
        except Exception:
            pass  # Ignore if no modal
        
        # Wait for job details to load
        try:
            await page.wait_for_selector('.jobDescriptionContent, .desc', timeout=10000)
        except TimeoutError:
            return None
        
        # Random delay
        await self._random_delay(1.0, 2.0)
        
        # Extract job description
        description_elem = await page.query_selector('.jobDescriptionContent, .desc')
        description = await description_elem.inner_text() if description_elem else ""
        
        # Try to extract additional details
        job_type_elem = await page.query_selector('span:has-text("Employment Type")')
        job_type = None
        if job_type_elem:
            job_type_container = await job_type_elem.evaluate('el => el.nextElementSibling')
            job_type = job_type_container.textContent if job_type_container else None
        
        return {
            'description': description,
            'job_type': job_type
        }