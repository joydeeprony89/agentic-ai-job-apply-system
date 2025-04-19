from typing import List, Dict, Any
from datetime import timedelta
from redis import Redis
from .job_analysis_agent import JobAnalysisAgent
from .search_strategy_agent import SearchStrategyAgent
from .crawlers import LinkedInCrawler, NaukriCrawler

class JobDiscoveryAgent:
    def __init__(self, groq_api_key: str):
        self.job_analyzer = JobAnalysisAgent(groq_api_key)
        self.strategy_agent = SearchStrategyAgent(groq_api_key)
        self.redis_client = Redis(host='localhost', port=6379, db=0)
        self.cache_ttl = timedelta(hours=1)
        self.crawlers = {
            'linkedin': LinkedInCrawler(),
            'naukri': NaukriCrawler()
        }

    async def search_jobs(self, keywords: List[str], location: str) -> List[Dict[str, Any]]:
        cache_key = f"jobs:{':'.join(keywords)}:{location}"
        
        # Check cache
        if cached_results := self.redis_client.get(cache_key):
            return cached_results

        # Get enhanced keywords using Groq
        enhanced_keywords = await self.job_analyzer.analyze_keywords(keywords)
        
        # Get optimal search strategy
        search_strategy = await self.strategy_agent.optimize_search_strategy(
            enhanced_keywords, 
            location
        )
        
        # Execute search based on strategy
        jobs = await self._execute_search(enhanced_keywords, location, search_strategy)
        
        # Analyze and categorize jobs
        analyzed_jobs = []
        for job in jobs:
            job_analysis = await self.job_analyzer.categorize_job(job['description'])
            analyzed_jobs.append({**job, 'analysis': job_analysis})
        
        # Cache results
        self.redis_client.setex(cache_key, self.cache_ttl, analyzed_jobs)
        
        return analyzed_jobs

    async def _execute_search(
        self, 
        keywords: List[str], 
        location: str, 
        strategy: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        all_jobs = []
        for source in strategy['platforms']:
            if crawler := self.crawlers.get(source):
                jobs = await crawler.search(keywords, location)
                all_jobs.extend(jobs)
        return all_jobs