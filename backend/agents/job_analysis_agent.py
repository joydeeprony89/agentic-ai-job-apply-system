from typing import List, Dict, Any
import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.llm_service import groq_service, LLMServiceError
from core.logging import get_logger

# Get logger
logger = get_logger(__name__)

class JobAnalysisAgent:
    def __init__(self, groq_api_key: str = None):
        """
        Initialize the Job Analysis Agent.
        
        Args:
            groq_api_key: Groq API key. If None, uses the one from settings.
        """
        # Pass the API key to the Groq service if provided
        if groq_api_key:
            self.groq_service = groq_service
            self.groq_service.api_key = groq_api_key
        else:
            self.groq_service = groq_service

    async def analyze_keywords(self, keywords: List[str]) -> List[str]:
        """
        Analyze keywords using Groq API.
        
        Args:
            keywords: List of keywords to analyze
            
        Returns:
            List of enhanced keywords
            
        Raises:
            LLMServiceError: If there's an error with the LLM service
        """
        logger.info(f"Analyzing keywords: {keywords}")
        prompt = self._create_keyword_analysis_prompt(keywords)
        
        # Call Groq API and extract list content
        response = await self.groq_service.generate_completion(prompt)
        return self.groq_service.extract_list_content(response)

    async def categorize_job(self, description: str) -> Dict[str, Any]:
        """
        Categorize job description using Groq API.
        
        Args:
            description: Job description to categorize
            
        Returns:
            Dictionary with job categories
            
        Raises:
            LLMServiceError: If there's an error with the LLM service
        """
        logger.info("Categorizing job description")
        prompt = self._create_job_analysis_prompt(description)
        
        # Call Groq API and extract JSON content
        response = await self.groq_service.generate_completion(prompt)
        return self.groq_service.extract_json_content(response)

    def _create_keyword_analysis_prompt(self, keywords: List[str]) -> str:
        """
        Create prompt for keyword analysis.
        
        Args:
            keywords: List of keywords to analyze
            
        Returns:
            Prompt string
        """
        return f"""
        Analyze the following job search keywords and suggest only the most relevant related terms.
        Focus strictly on technical skills, modern job titles, and industry-specific terminology used in job descriptions.
        Avoid generic terms, synonyms, or overly broad concepts.
        
        Do not include any explanation or introductory text.
        Only return a concise, comma-separated list of 10–15 high-impact keywords only, list without additional commentary. 

        Example output: ["python", "machine learning", "data science"].
        Keywords: {', '.join(keywords)}
        Suggest only closely related keywords that would improve search results on job boards like LinkedIn, Indeed, Naukri, Glassdoor, or Glassdoor.
        Limit results to job-relevant technical skills, roles, and industry jargon.
        Do not include certifications, tools unless core to the keyword.
        """

    def _create_job_analysis_prompt(self, description: str) -> str:
        """
        Create prompt for job analysis.
        
        Args:
            description: Job description to analyze
            
        Returns:
            Prompt string
        """
        return f"""
        Analyze this job description and extract:
        1. Required skills (technical and soft)
        2. Experience level (junior, mid, senior)
        3. Job category (e.g., frontend, backend, fullstack)
        4. Key responsibilities
        5. Nice-to-have skills

        Description: {description}
        
        Format: Return as a JSON object with these fields.
        """