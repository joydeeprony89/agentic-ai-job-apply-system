"""
Agent routes for the API.

This module contains all the routes related to the agent functionality,
including job discovery, keyword analysis, and search strategy optimization.
"""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from fastapi import APIRouter, HTTPException, status, Query, Depends

from core.config import settings
from core.logging import get_logger
from agents.job_discovery import JobDiscoveryAgent
from api.deps import verify_api_key

# Get logger
logger = get_logger(__name__)

router = APIRouter()

# Initialize agents
job_discovery_agent = JobDiscoveryAgent(settings.GROQ_API_KEY)


class JobSearchRequest(BaseModel):
    """Job search request model."""
    keywords: List[str] = Field(
        ..., 
        description="List of keywords related to the job search",
        example=["python", "machine learning", "data science"]
    )
    location: str = Field(
        ..., 
        description="Location for the job search",
        example="San Francisco, CA"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "keywords": ["python", "machine learning", "data science"],
                "location": "San Francisco, CA"
            }
        }


class JobResponse(BaseModel):
    """Job response model."""
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    location: str = Field(..., description="Job location")
    description: str = Field(..., description="Job description")
    url: str = Field(..., description="Job posting URL")
    platform: str = Field(..., description="Job platform (LinkedIn, Indeed, etc.)")
    date_posted: Optional[str] = Field(None, description="Date when the job was posted")
    salary: Optional[str] = Field(None, description="Salary information if available")
    job_type: Optional[str] = Field(None, description="Job type (Full-time, Part-time, etc.)")
    
    class Config:
        schema_extra = {
            "example": {
                "title": "Senior Python Developer",
                "company": "Tech Solutions Inc.",
                "location": "San Francisco, CA",
                "description": "We are looking for a Senior Python Developer...",
                "url": "https://example.com/job/123",
                "platform": "LinkedIn",
                "date_posted": "2023-05-15",
                "salary": "$120,000 - $150,000",
                "job_type": "Full-time"
            }
        }


class JobSearchResponse(BaseModel):
    """Job search response model."""
    success: bool = Field(..., description="Whether the request was successful")
    count: int = Field(..., description="Number of jobs found")
    jobs: List[Dict[str, Any]] = Field(..., description="List of jobs")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "count": 2,
                "jobs": [
                    {
                        "title": "Senior Python Developer",
                        "company": "Tech Solutions Inc.",
                        "location": "San Francisco, CA",
                        "description": "We are looking for a Senior Python Developer...",
                        "url": "https://example.com/job/123",
                        "platform": "LinkedIn",
                        "date_posted": "2023-05-15",
                        "salary": "$120,000 - $150,000",
                        "job_type": "Full-time"
                    },
                    {
                        "title": "Machine Learning Engineer",
                        "company": "AI Innovations",
                        "location": "San Francisco, CA",
                        "description": "Join our team of ML engineers...",
                        "url": "https://example.com/job/456",
                        "platform": "Indeed",
                        "date_posted": "2023-05-10",
                        "salary": "$130,000 - $160,000",
                        "job_type": "Full-time"
                    }
                ]
            }
        }


@router.post(
    "/job-discovery/search", 
    response_model=JobSearchResponse,
    status_code=status.HTTP_200_OK,
    summary="Search for jobs",
    dependencies=[Depends(verify_api_key)],
    description="""
    Search for jobs using the Job Discovery Agent.
    
    The agent will:
    1. Analyze and enhance the provided keywords
    2. Determine the optimal search strategy
    3. Execute concurrent searches across multiple job platforms
    4. Return the most relevant job listings
    
    This endpoint leverages:
    - Autonomous Search Planning
    - Adaptive Crawling
    - Query Refinement
    - Distributed Crawling
    - Rate Limiting
    """
)
async def search_jobs(
    request: JobSearchRequest
) -> Dict[str, Any]:
    """
    Search for jobs using the Job Discovery Agent.
    
    Args:
        request: Job search request with keywords and location
        
    Returns:
        Dictionary with search results
    """
    logger.info(f"Job search request received: keywords={request.keywords}, location={request.location}")
    
    try:
        # Execute job search
        jobs = await job_discovery_agent.search_jobs(
            keywords=request.keywords,
            location=request.location
        )
        
        logger.info(f"Job search completed successfully: found {len(jobs)} jobs")
        
        return {
            "success": True,
            "count": len(jobs),
            "jobs": jobs
        }
    except Exception as e:
        logger.error(f"Error searching jobs: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching jobs: {str(e)}"
        )


class PlatformStats(BaseModel):
    """Platform statistics model."""
    success_rate: float = Field(..., description="Success rate of the platform")
    avg_response_time: float = Field(..., description="Average response time in seconds")
    job_count: int = Field(..., description="Number of jobs found")
    last_crawl_time: Optional[str] = Field(None, description="Last time the platform was crawled")
    
    class Config:
        schema_extra = {
            "example": {
                "success_rate": 0.95,
                "avg_response_time": 2.3,
                "job_count": 150,
                "last_crawl_time": "2023-05-15T14:30:00Z"
            }
        }


class StatsResponse(BaseModel):
    """Statistics response model."""
    success: bool = Field(..., description="Whether the request was successful")
    stats: Dict[str, PlatformStats] = Field(..., description="Platform statistics")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "stats": {
                    "linkedin": {
                        "success_rate": 0.95,
                        "avg_response_time": 2.3,
                        "job_count": 150,
                        "last_crawl_time": "2023-05-15T14:30:00Z"
                    },
                    "indeed": {
                        "success_rate": 0.92,
                        "avg_response_time": 1.8,
                        "job_count": 120,
                        "last_crawl_time": "2023-05-15T14:35:00Z"
                    }
                }
            }
        }


@router.get(
    "/job-discovery/stats", 
    response_model=StatsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get job discovery statistics",
    dependencies=[Depends(verify_api_key)],
    description="""
    Get statistics about the job discovery process.
    
    Returns performance metrics for each job platform, including:
    - Success rate
    - Average response time
    - Number of jobs found
    - Last crawl time
    
    This information is used by the Adaptive Crawling technique to optimize platform selection.
    """
)
async def get_job_discovery_stats() -> Dict[str, Any]:
    """
    Get job discovery statistics.
    
    Returns:
        Dictionary with job discovery statistics
    """
    logger.info("Request received for job discovery statistics")
    
    try:
        stats = await job_discovery_agent.get_platform_stats()
        
        logger.info(f"Retrieved statistics for {len(stats)} platforms")
        
        return {
            "success": True,
            "stats": stats
        }
    except Exception as e:
        logger.error(f"Error getting job discovery stats: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting job discovery stats: {str(e)}"
        )


class KeywordAnalysisRequest(BaseModel):
    """Keyword analysis request model."""
    keywords: List[str] = Field(
        ..., 
        description="List of keywords to analyze",
        example=["python", "machine learning"]
    )
    
    class Config:
        schema_extra = {
            "example": {
                "keywords": ["python", "machine learning"]
            }
        }


class KeywordAnalysisResponse(BaseModel):
    """Keyword analysis response model."""
    success: bool = Field(..., description="Whether the request was successful")
    original_keywords: List[str] = Field(..., description="Original keywords")
    enhanced_keywords: List[str] = Field(..., description="Enhanced keywords")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "original_keywords": ["python", "machine learning"],
                "enhanced_keywords": [
                    "python", 
                    "machine learning", 
                    "data science", 
                    "deep learning", 
                    "TensorFlow", 
                    "PyTorch", 
                    "scikit-learn"
                ]
            }
        }


@router.post(
    "/job-discovery/analyze-keywords", 
    response_model=KeywordAnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Analyze and enhance keywords",
    dependencies=[Depends(verify_api_key)],
    description="""
    Analyze keywords using the Job Analysis Agent.
    
    The agent will:
    1. Analyze the provided keywords
    2. Expand them with related terms
    3. Add industry-specific terminology
    4. Return the enhanced keyword set
    
    This endpoint implements the Query Refinement technique.
    """
)
async def analyze_keywords(
    request: KeywordAnalysisRequest
) -> Dict[str, Any]:
    """
    Analyze keywords using the Job Analysis Agent.
    
    Args:
        request: Keyword analysis request with keywords
        
    Returns:
        Dictionary with analyzed keywords
    """
    try:
        enhanced_keywords = await job_discovery_agent.job_analyzer.analyze_keywords(request.keywords)
        return {
            "success": True,
            "original_keywords": request.keywords,
            "enhanced_keywords": enhanced_keywords
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing keywords: {str(e)}"
        )


class StrategyOptimizationRequest(BaseModel):
    """Strategy optimization request model."""
    keywords: List[str] = Field(
        ..., 
        description="List of keywords for strategy optimization",
        example=["python", "machine learning", "data science"]
    )
    location: str = Field(
        ..., 
        description="Location for strategy optimization",
        example="San Francisco, CA"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "keywords": ["python", "machine learning", "data science"],
                "location": "San Francisco, CA"
            }
        }


class PlatformStrategy(BaseModel):
    """Platform strategy model."""
    priority: int = Field(..., description="Priority of the platform (lower is higher priority)")
    keywords: List[str] = Field(..., description="Keywords to use for this platform")
    filters: Dict[str, Any] = Field(..., description="Filters to apply for this platform")
    
    class Config:
        schema_extra = {
            "example": {
                "priority": 1,
                "keywords": ["python", "machine learning", "data science", "TensorFlow"],
                "filters": {
                    "job_type": "full-time",
                    "experience_level": "mid-senior",
                    "date_posted": "past_week"
                }
            }
        }


class StrategyResponse(BaseModel):
    """Strategy response model."""
    success: bool = Field(..., description="Whether the request was successful")
    original_keywords: List[str] = Field(..., description="Original keywords")
    enhanced_keywords: List[str] = Field(..., description="Enhanced keywords")
    strategy: Dict[str, PlatformStrategy] = Field(..., description="Search strategy for each platform")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "original_keywords": ["python", "machine learning"],
                "enhanced_keywords": ["python", "machine learning", "data science", "TensorFlow", "PyTorch"],
                "strategy": {
                    "linkedin": {
                        "priority": 1,
                        "keywords": ["python", "machine learning", "data science", "TensorFlow"],
                        "filters": {
                            "job_type": "full-time",
                            "experience_level": "mid-senior",
                            "date_posted": "past_week"
                        }
                    },
                    "indeed": {
                        "priority": 2,
                        "keywords": ["python developer", "machine learning engineer", "data scientist"],
                        "filters": {
                            "job_type": "full-time",
                            "date_posted": "past_month"
                        }
                    }
                }
            }
        }


@router.post(
    "/job-discovery/optimize-strategy", 
    response_model=StrategyResponse,
    status_code=status.HTTP_200_OK,
    summary="Optimize search strategy",
    dependencies=[Depends(verify_api_key)],
    description="""
    Optimize search strategy using the Search Strategy Agent.
    
    The agent will:
    1. Analyze platform performance metrics
    2. Enhance the provided keywords
    3. Create a tailored search strategy for each platform
    4. Prioritize platforms based on past performance
    
    This endpoint implements the Autonomous Search Planning technique.
    """
)
async def optimize_search_strategy(
    request: StrategyOptimizationRequest
) -> Dict[str, Any]:
    """
    Optimize search strategy using the Search Strategy Agent.
    
    Args:
        request: Strategy optimization request with keywords and location
        
    Returns:
        Dictionary with optimized search strategy
    """
    try:
        # Get platform performance from job discovery agent
        platform_performance = job_discovery_agent.platform_performance
        
        # Get enhanced keywords
        enhanced_keywords = await job_discovery_agent.job_analyzer.analyze_keywords(request.keywords)
        
        # Get search strategy
        strategy = await job_discovery_agent.strategy_agent.optimize_search_strategy(
            enhanced_keywords,
            request.location,
            platform_performance
        )
        
        return {
            "success": True,
            "original_keywords": request.keywords,
            "enhanced_keywords": enhanced_keywords,
            "strategy": strategy
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error optimizing search strategy: {str(e)}"
        )