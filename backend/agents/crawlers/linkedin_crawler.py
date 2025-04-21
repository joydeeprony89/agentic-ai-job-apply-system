from typing import List, Dict, Any, Optional
import re
import json
from datetime import datetime, timedelta
from urllib.parse import quote
from playwright.async_api import TimeoutError

from core.mongodb import store_job_listings, update_crawl_stats
from core.vector_store import batch_index_jobs
from .base_crawler import BaseCrawler


class LinkedInCrawler(BaseCrawler):
    """
    LinkedIn job crawler.
    """
    def __init__(self):
        super().__init__(domain="linkedin.com")
        self.base_url = "https://www.linkedin.com/jobs/search"
    
    async def search(self, keywords: List[str], location: str) -> List[Dict[str, Any]]:
        """
        Search for jobs on LinkedIn.
        
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
                search_url = f"{self.base_url}/?keywords={quote(keyword_string)}&location={quote(location)}&f_TPR=r86400&sortBy=DD"
                
                # Navigate to LinkedIn jobs
                if not await self._navigate(page, search_url):
                    self.update_stats(False)
                    return []
                
                # Wait for results
                try:
                    print("Waiting for job results to load...")
                    await page.wait_for_selector('.job-card-container', timeout=10000)
                    print("Job results loaded successfully")
                except TimeoutError:
                    print("Timeout waiting for job-card-container, trying alternative selector")
                    # Try an alternative selector
                    try:
                        await page.wait_for_selector('.jobs-search__results-list li', timeout=5000)
                        print("Job results loaded with alternative selector")
                    except TimeoutError:
                        print("Timeout waiting for jobs-search__results-list li")
                        # Try one more alternative selector
                        try:
                            await page.wait_for_selector('[data-job-id], [data-entity-urn*="jobPosting"]', timeout=5000)
                            print("Job results loaded with data attribute selector")
                        except TimeoutError:
                            print("No job results found after all selector attempts")
                            self.update_stats(False)
                            return []
                
                # Random delay to simulate human behavior
                await self._random_delay(2.0, 4.0)
                
                # Extract job listings
                try:
                    job_cards = await page.query_selector_all('.job-card-container, .jobs-search__results-list li')
                    
                    if not job_cards or len(job_cards) == 0:
                        print("No job cards found on the page")
                        # Try an alternative approach - look for any job-related elements
                        job_cards = await page.query_selector_all('[data-job-id], [data-entity-urn*="jobPosting"]')
                        
                    print(f"Found {len(job_cards)} job cards")
                    
                    for card in job_cards:
                        try:
                            # Extract basic job info
                            title_elem = await card.query_selector('.job-card-list__title, .base-search-card__title, .job-title')
                            company_elem = await card.query_selector('.job-card-container__company-name, .base-search-card__subtitle, .company-name')
                            location_elem = await card.query_selector('.job-card-container__metadata-item, .job-search-card__location, .job-location')
                            link_elem = await card.query_selector('a')
                            
                            if not title_elem or not link_elem:
                                print("Missing title or link element, skipping job card")
                                continue
                            
                            title = await title_elem.inner_text()
                            company = await company_elem.inner_text() if company_elem else "Unknown Company"
                            job_location = await location_elem.inner_text() if location_elem else location
                            url = await link_elem.get_attribute('href')
                            
                            # Extract job ID from URL
                            job_id_match = re.search(r'(?:jobs|view)/(\d+)', url)
                            job_id = job_id_match.group(1) if job_id_match else None
                            
                            if not job_id:
                                # Try alternative ID extraction
                                job_id = await card.get_attribute('data-job-id') or await card.get_attribute('data-entity-urn')
                                if job_id and 'jobPosting:' in job_id:
                                    job_id = job_id.split('jobPosting:')[-1]
                                
                                if not job_id:
                                    print("Could not extract job ID, skipping job card")
                                    continue
                            
                            # Basic job data
                            job = {
                                'title': title.strip(),
                                'company': company.strip(),
                                'location': job_location.strip(),
                                'url': url,
                                'external_id': f"linkedin-{job_id}",
                                'source': 'linkedin',
                                'crawl_date': datetime.now().isoformat(),
                                'keywords': keywords,
                                'description': ""  # Will be filled in detail crawl
                            }
                            
                            jobs.append(job)
                            print(f"Added job: {job['title']} at {job['company']}")
                            
                            # Limit to 20 jobs per search to avoid overloading
                            if len(jobs) >= 20:
                                break
                        
                        except Exception as e:
                            print(f"Error extracting job card: {e}")
                            continue
                except Exception as e:
                    print(f"Error extracting job listings: {e}")
                    search_success = False
                
                # Get job details for each job
                detailed_jobs = []
                if jobs:
                    print(f"Getting details for {min(5, len(jobs))} jobs")
                    for job in jobs[:5]:  # Limit detailed crawls to 5 jobs
                        try:
                            print(f"Getting details for job: {job['title']} at {job['company']}")
                            job_details = await self._get_job_details(page, job['url'])
                            if job_details:
                                detailed_job = {**job, **job_details}
                                detailed_jobs.append(detailed_job)
                                print(f"Successfully got details for job: {job['title']}")
                            else:
                                print(f"No details found for job: {job['title']}")
                                detailed_jobs.append(job)
                        except Exception as e:
                            print(f"Error getting job details: {e}")
                            detailed_jobs.append(job)
                    
                    # Store jobs in MongoDB
                    if detailed_jobs:
                        print(f"Storing {len(detailed_jobs)} jobs in MongoDB")
                        try:
                            await store_job_listings(detailed_jobs)
                            
                            # Index jobs in vector database
                            print(f"Indexing {len(detailed_jobs)} jobs in vector database")
                            await batch_index_jobs(detailed_jobs)
                        except Exception as e:
                            print(f"Error storing or indexing jobs: {e}")
                    
                    search_success = True
                    jobs = detailed_jobs + jobs[5:]  # Combine detailed and non-detailed jobs
                    print(f"Total jobs found: {len(jobs)}")
                else:
                    print("No jobs found to get details for")
        
        except Exception as e:
            print(f"LinkedIn crawler error: {e}")
            import traceback
            traceback.print_exc()
            search_success = False
        
        # Update crawler stats
        self.update_stats(search_success)
        await update_crawl_stats("linkedin", 
                                len(jobs) if search_success else 0,
                                0 if search_success else 1, 
                                keywords)
        
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
            await page.wait_for_selector('.jobs-description-content, .description__text', timeout=10000)
        except TimeoutError:
            return None
        
        # Random delay
        await self._random_delay(1.0, 2.0)
        
        # Extract job description
        description_elem = await page.query_selector('.jobs-description-content, .description__text')
        description = ""
        if description_elem:
            try:
                description = await description_elem.inner_text()
            except Exception as e:
                print(f"Error extracting description: {e}")
        
        # Extract additional details
        details = {}
        
        # Try to extract salary
        try:
            salary_elem = await page.query_selector('.compensation-information, .jobs-unified-top-card__job-insight span:has-text("$")')
            if salary_elem:
                salary_text = await salary_elem.inner_text()
                details['salary_text'] = salary_text
        except Exception as e:
            print(f"Error extracting salary: {e}")
        
        # Try to extract job type
        try:
            job_type_elem = await page.query_selector('.jobs-unified-top-card__job-insight:has-text("Employment type")')
            if job_type_elem:
                job_type = await job_type_elem.inner_text()
                details['job_type'] = job_type.replace('Employment type', '').strip()
        except Exception as e:
            print(f"Error extracting job type: {e}")
        
        # Try to extract posting date
        try:
            date_elem = await page.query_selector('.jobs-unified-top-card__posted-date, .posted-time-ago__text')
            if date_elem:
                posted_date = await date_elem.inner_text()
                details['posted_date_text'] = posted_date
        except Exception as e:
            print(f"Error extracting posting date: {e}")
        
        return {
            'description': description,
            'details': details
        }