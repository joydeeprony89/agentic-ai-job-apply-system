"""
MongoDB configuration and connection management.

This module is modified to work without an actual MongoDB connection for development purposes.
In a production environment, this would connect to a real MongoDB instance.
"""
from typing import Dict, Any, List
import os
import json
from datetime import datetime
import uuid

from core.config import settings

# In-memory storage for development
job_listings = []
crawl_stats = {}


async def store_job_listings(jobs: List[Dict[str, Any]]) -> List[str]:
    """
    Store job listings in memory.
    Returns the inserted document IDs.
    """
    if not jobs:
        return []
    
    inserted_ids = []
    
    # Add metadata and prepare for storage
    for job in jobs:
        if 'external_id' not in job and 'url' in job:
            # Create a unique ID if not present
            job['external_id'] = job['url'].split('/')[-1]
        
        # Add an ID
        job_id = str(uuid.uuid4())
        job['_id'] = job_id
        inserted_ids.append(job_id)
        
        # Store in memory
        job_listings.append(job)
    
    return inserted_ids


async def get_job_listing(job_id: str) -> Dict[str, Any]:
    """
    Get a job listing by ID.
    """
    for job in job_listings:
        if job.get('_id') == job_id:
            return job
    return None


async def get_job_listings_by_query(query: Dict[str, Any], limit: int = 100) -> List[Dict[str, Any]]:
    """
    Get job listings by query.
    
    This is a simplified version that doesn't actually filter by query.
    In a real implementation, this would use MongoDB's query capabilities.
    """
    return job_listings[:limit]


async def update_crawl_stats(source: str, success_count: int, error_count: int, keywords: List[str]) -> None:
    """
    Update crawl statistics.
    
    Args:
        source: Source of the crawl (e.g., 'linkedin')
        success_count: Number of successful crawls
        error_count: Number of failed crawls
        keywords: Keywords used for the crawl
    """
    if source not in crawl_stats:
        crawl_stats[source] = {
            "source": source,
            "total_crawls": 0,
            "success_count": 0,
            "error_count": 0,
            "last_crawl_time": None,
            "last_keywords": []
        }
    
    stats = crawl_stats[source]
    stats["total_crawls"] += 1
    stats["success_count"] += success_count
    stats["error_count"] += error_count
    stats["last_crawl_time"] = datetime.now().isoformat()
    stats["last_keywords"] = keywords


async def get_crawl_stats(source: str = None) -> List[Dict[str, Any]]:
    """
    Get crawl statistics.
    """
    if source:
        return [crawl_stats.get(source, {"source": source, "total_crawls": 0, "success_count": 0, "error_count": 0})]
    return list(crawl_stats.values())