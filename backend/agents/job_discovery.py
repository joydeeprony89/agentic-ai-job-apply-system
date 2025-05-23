from typing import List, Dict, Any, Optional
import time
import sys
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from datetime import datetime
import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.config import settings
from core.logging import get_logger
from services.llm_service import groq_service
from services.llm_service import groq_service
from .job_analysis_agent import JobAnalysisAgent
from .search_strategy_agent import SearchStrategyAgent
from .crawlers import LinkedInCrawler, NaukriCrawler
from .crawlers.indeed_crawler import IndeedCrawler
from .crawlers.glassdoor_crawler import GlassdoorCrawler

# Configure event loop policy for Windows
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Get logger
logger = get_logger(__name__)


class JobDiscoveryAgent:
    """
    Agent responsible for discovering job listings across multiple platforms.
    Performs real-time searches without data storage.
    """
    def __init__(self, groq_api_key: str = None):
        """
        Initialize the Job Discovery Agent.
        
        Args:
            groq_api_key: Groq API key. If None, uses the one from settings.
        """
        # Pass the API key to the Groq service if provided
        if groq_api_key:
            self.groq_service = groq_service
            self.groq_service.api_key = groq_api_key
        else:
            self.groq_service = groq_service
            
        self.job_analyzer = JobAnalysisAgent(groq_api_key)
        self.strategy_agent = SearchStrategyAgent(groq_api_key)
        
        # Initialize crawlers
        self.crawlers = {
            'linkedin': LinkedInCrawler(),
            'naukri': NaukriCrawler(),
            'indeed': IndeedCrawler(),
            'glassdoor': GlassdoorCrawler(),
        }
        
        # Default platform performance metrics
        self.platform_performance = {
            'linkedin': {'success_rate': 0.9, 'avg_results': 15, 'avg_time': 10},
            'indeed': {'success_rate': 0.8, 'avg_results': 20, 'avg_time': 12},
            'naukri': {'success_rate': 0.7, 'avg_results': 10, 'avg_time': 8},
            'glassdoor': {'success_rate': 0.6, 'avg_results': 12, 'avg_time': 15},
        }

    async def search_jobs(
        self, 
        keywords: List[str], 
        location: str,
    ) -> List[Dict[str, Any]]:
        """
        Search for jobs across multiple platforms in real-time.
        
        Args:
            keywords: List of search keywords
            location: Job location
            
        Returns:
            List of job dictionaries
        """
        # Start timing the search
        start_time = time.time()
        
        # Get enhanced keywords using Groq
        enhanced_keywords = await self.job_analyzer.analyze_keywords(keywords)
        logger.info(f"Enhanced keywords: {enhanced_keywords}")
        
        # Get optimal search strategy based on default performance metrics
        search_strategy = await self.strategy_agent.optimize_search_strategy(
            enhanced_keywords, 
            location,
            self.platform_performance
        )
        logger.info(f"Search strategy: {search_strategy}")
        
        # Execute search based on strategy
        jobs = await self._execute_search(enhanced_keywords, location, search_strategy)
        logger.info(f"Found {len(jobs)} jobs from crawlers")
        
        # Remove duplicates by URL
        unique_jobs = {}
        for job in jobs:
            job_id = job.get('url')
            if job_id and job_id not in unique_jobs:
                unique_jobs[job_id] = job
        
        # Convert back to list
        unique_jobs_list = list(unique_jobs.values())
        
        # Analyze and categorize jobs (limit to 10 for performance)
        analyzed_jobs = []
        for job in unique_jobs_list[:10]:
            if job.get('description'):
                job_analysis = await self.job_analyzer.categorize_job(job['description'])
                analyzed_jobs.append({**job, 'analysis': job_analysis})
            else:
                analyzed_jobs.append(job)
        
        # Add remaining jobs without analysis
        analyzed_jobs.extend(unique_jobs_list[10:])
        
        # Log search time
        search_time = time.time() - start_time
        logger.info(f"Search completed in {search_time:.2f} seconds")
        
        return analyzed_jobs

    async def _execute_search(
        self, 
        keywords: List[str], 
        location: str, 
        strategy: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Execute job search across multiple platforms.
        
        Args:
            keywords: List of search keywords
            location: Job location
            strategy: Search strategy
            
        Returns:
            List of job dictionaries
        """
        all_jobs = []
        tasks = []
        
        # Create tasks for crawler-based platforms
        for source in strategy.get("platforms", []):
            if crawler := self.crawlers.get(source):
                logger.info(f"Creating search task for {source}")
                # Create coroutine but don't schedule it yet
                coro = crawler.search(keywords, location)
                tasks.append((source, coro))
        
        if not tasks:
            logger.warning("No valid platforms found for search")
            return []
            
        # Execute crawler tasks concurrently with limit
        max_concurrent = min(len(tasks), 3)  # Limit to 3 concurrent crawlers
        logger.info(f"Executing {len(tasks)} search tasks with max concurrency of {max_concurrent}")
        
        try:
            # Process tasks in batches to limit concurrency
            for i in range(0, len(tasks), max_concurrent):
                batch = tasks[i:i+max_concurrent]
                batch_tasks = [asyncio.create_task(coro) for _, coro in batch]
                batch_sources = [source for source, _ in batch]
                
                # Wait for all tasks in this batch to complete
                batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)
                
                # Process results
                for j, result in enumerate(batch_results):
                    source = batch_sources[j]
                    if isinstance(result, Exception):
                        logger.error(f"Error in {source} crawler: {result}")
                        import traceback
                        logger.error(''.join(traceback.format_exception(type(result), result, result.__traceback__)))
                    else:
                        job_count = len(result) if isinstance(result, list) else 0
                        logger.info(f"Found {job_count} jobs from {source}")
                        if job_count > 0:
                            all_jobs.extend(result)
        except Exception as e:
            logger.error(f"Error executing search tasks: {e}")
            import traceback
            logger.error(traceback.format_exc())
        
        logger.info(f"Total jobs found across all platforms: {len(all_jobs)}")
        return all_jobs
    
    async def get_platform_stats(self) -> Dict[str, Any]:
        """
        Get platform statistics.
        
        Returns:
            Dictionary with platform statistics
        """
        return {
            'performance': self.platform_performance,
            'available_platforms': list(self.crawlers.keys())
        }