"""
Indeed job crawler.
"""
from typing import List, Dict, Any, Optional
import re
from urllib.parse import quote
from datetime import datetime
from playwright.async_api import TimeoutError

from .base_crawler import BaseCrawler


class IndeedCrawler(BaseCrawler):
    """
    Indeed job crawler.
    """
    def __init__(self):
        super().__init__(domain="indeed.com")
        self.base_url = "https://www.indeed.com/jobs"
    
    async def search(self, keywords: List[str], location: str) -> List[Dict[str, Any]]:
        """
        Search for jobs on Indeed.
        
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
                search_url = f"{self.base_url}?q={quote(keyword_string)}&l={quote(location)}&sort=date"
                
                # Navigate to Indeed jobs
                if not await self._navigate(page, search_url):
                    self.update_stats(False)
                    return []
                
                # Wait for results
                try:
                    await page.wait_for_selector('.job_seen_beacon, .jobsearch-ResultsList .result', timeout=10000)
                except TimeoutError:
                    self.update_stats(False)
                    return []
                
                # Random delay to simulate human behavior
                await self._random_delay(2.0, 4.0)
                
                # Extract job listings
                job_cards = await page.query_selector_all('.job_seen_beacon, .jobsearch-ResultsList .result')
                
                for card in job_cards:
                    try:
                        # Extract basic job info
                        title_elem = await card.query_selector('h2.jobTitle, .jcs-JobTitle')
                        company_elem = await card.query_selector('.companyName, .companyOverviewLink')
                        location_elem = await card.query_selector('.companyLocation')
                        link_elem = await card.query_selector('h2.jobTitle a, .jcs-JobTitle a')
                        
                        if not title_elem or not link_elem:
                            continue
                        
                        title = await title_elem.inner_text()
                        company = await company_elem.inner_text() if company_elem else "Unknown Company"
                        job_location = await location_elem.inner_text() if location_elem else location
                        
                        # Get the relative URL and convert to absolute
                        relative_url = await link_elem.get_attribute('href')
                        url = f"https://www.indeed.com{relative_url}" if relative_url.startswith('/') else relative_url
                        
                        # Extract job ID from URL
                        job_id_match = re.search(r'jk=([a-zA-Z0-9]+)', url)
                        job_id = job_id_match.group(1) if job_id_match else None
                        
                        if not job_id:
                            continue
                        
                        # Try to extract salary if available
                        salary_elem = await card.query_selector('.salary-snippet-container, .metadataContainer .attribute:has-text("$")')
                        salary = await salary_elem.inner_text() if salary_elem else None
                        
                        # Try to extract job type
                        job_type_elem = await card.query_selector('.metadata:has-text("Full-time"), .metadata:has-text("Part-time")')
                        job_type = await job_type_elem.inner_text() if job_type_elem else None
                        
                        # Basic job data
                        job = {
                            'title': title.strip(),
                            'company': company.strip(),
                            'location': job_location.strip(),
                            'url': url,
                            'source': 'indeed',
                            'search_date': datetime.now().isoformat(),
                            'salary': salary.strip() if salary else None,
                            'job_type': job_type.strip() if job_type else None,
                        }
                        
                        jobs.append(job)
                        
                        # Limit to 20 jobs per search to avoid overloading
                        if len(jobs) >= 20:
                            break
                    
                    except Exception as e:
                        print(f"Error extracting Indeed job card: {e}")
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
                        print(f"Error getting Indeed job details: {e}")
                        detailed_jobs.append(job)
                
                search_success = True
                jobs = detailed_jobs + jobs[5:]  # Combine detailed and non-detailed jobs
        
        except Exception as e:
            print(f"Indeed crawler error: {e}")
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
        
        # Wait for job details to load
        try:
            await page.wait_for_selector('#jobDescriptionText', timeout=10000)
        except TimeoutError:
            return None
        
        # Random delay
        await self._random_delay(1.0, 2.0)
        
        # Extract job description
        description_elem = await page.query_selector('#jobDescriptionText')
        description = await description_elem.inner_text() if description_elem else ""
        
        return {
            'description': description
        }