"""
Vector database integration for semantic search.

This module is modified to work without an actual vector database connection for development purposes.
In a production environment, this would connect to a real vector database like Pinecone.
"""
from typing import Dict, Any, List, Optional, Tuple
import random

# In-memory storage for development
indexed_jobs = []


def get_embedding(text: str) -> List[float]:
    """
    Mock function to simulate getting embeddings.
    
    Args:
        text: Text to embed
        
    Returns:
        Mock embedding vector
    """
    # Return a random vector of length 768 to simulate embeddings
    return [random.random() for _ in range(768)]


async def index_job(
    job_id: str,
    job_title: str,
    job_description: str,
    company: str,
    location: str,
    metadata: Dict[str, Any]
) -> bool:
    """
    Mock function to simulate indexing a job.
    
    Args:
        job_id: Job ID
        job_title: Job title
        job_description: Job description
        company: Company name
        location: Job location
        metadata: Additional metadata
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Create combined text for embedding
        combined_text = f"{job_title} {company} {location} {job_description}"
        
        # Get mock embedding
        embedding = get_embedding(combined_text)
        
        # Prepare metadata
        meta = {
            "job_id": job_id,
            "title": job_title,
            "company": company,
            "location": location,
            **metadata
        }
        
        # Store in memory
        indexed_jobs.append({
            "id": job_id,
            "embedding": embedding,
            "metadata": meta
        })
        
        return True
    except Exception as e:
        print(f"Error indexing job: {e}")
        return False


async def semantic_job_search(
    query: str,
    location: Optional[str] = None,
    top_k: int = 10
) -> List[Dict[str, Any]]:
    """
    Mock function to simulate semantic job search.
    
    Args:
        query: Search query
        location: Optional location filter
        top_k: Number of results to return
        
    Returns:
        List of matching jobs with scores
    """
    try:
        # Filter by location if provided
        filtered_jobs = indexed_jobs
        if location:
            filtered_jobs = [job for job in indexed_jobs if job["metadata"].get("location") == location]
        
        # Sort randomly to simulate semantic search
        random.shuffle(filtered_jobs)
        
        # Return top_k results
        matches = []
        for job in filtered_jobs[:top_k]:
            matches.append({
                "job_id": job["id"],
                "score": random.random(),  # Random score between 0 and 1
                "metadata": job["metadata"]
            })
        
        return matches
    except Exception as e:
        print(f"Error searching jobs: {e}")
        return []


async def batch_index_jobs(jobs: List[Dict[str, Any]]) -> Tuple[int, int]:
    """
    Mock function to simulate batch indexing of jobs.
    
    Args:
        jobs: List of job dictionaries
        
    Returns:
        Tuple of (success_count, error_count)
    """
    if not jobs:
        return 0, 0
    
    success_count = 0
    error_count = 0
    
    for job in jobs:
        try:
            job_id = job.get("id") or job.get("external_id")
            if not job_id:
                error_count += 1
                continue
                
            # Create combined text for embedding
            combined_text = f"{job.get('title', '')} {job.get('company', '')} {job.get('location', '')} {job.get('description', '')}"
            
            # Get mock embedding
            embedding = get_embedding(combined_text)
            
            # Prepare metadata (exclude large fields)
            meta = {k: v for k, v in job.items() if k != 'description' and isinstance(v, (str, int, float, bool))}
            
            # Store in memory
            indexed_jobs.append({
                "id": str(job_id),
                "embedding": embedding,
                "metadata": meta
            })
            
            success_count += 1
        except Exception as e:
            print(f"Error preparing job for indexing: {e}")
            error_count += 1
    
    return success_count, error_count