from typing import List, Dict, Any, Optional
import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.llm_service import groq_service, LLMServiceError
from core.config import settings
from core.logging import get_logger

# Get logger
logger = get_logger(__name__)

class SearchStrategyAgent:
    """
    Agent responsible for determining optimal job search strategies.
    """
    def __init__(self, groq_api_key: str = None):
        """
        Initialize the Search Strategy Agent.
        
        Args:
            groq_api_key: Groq API key. If None, uses the one from settings.
        """
        # Pass the API key to the Groq service if provided
        if groq_api_key:
            self.groq_service = groq_service
            self.groq_service.api_key = groq_api_key
        else:
            self.groq_service = groq_service
            
        self.available_platforms = [
            "linkedin", "indeed", "glassdoor", "naukri", "monster", 
            "ziprecruiter", "dice", "stackoverflow"
        ]

    async def optimize_search_strategy(
        self, 
        keywords: List[str], 
        location: str,
        platform_performance: Optional[Dict[str, Dict[str, float]]] = None
    ) -> Dict[str, Any]:
        """
        Determine the optimal search strategy based on keywords, location, and platform performance.
        
        Args:
            keywords: List of search keywords
            location: Job location
            platform_performance: Dictionary of platform performance metrics
            
        Returns:
            Dictionary with search strategy
            
        Raises:
            LLMServiceError: If there's an error with the LLM service
        """
        logger.info(f"Optimizing search strategy for keywords={keywords}, location={location}")
        prompt = self._create_strategy_prompt(keywords, location, platform_performance)
        
        # Call Groq API and extract JSON content
        response = await self.groq_service.generate_completion(prompt)
        
        try:
            strategy = self.groq_service.extract_json_content(response)
        except LLMServiceError:
            # If JSON parsing fails, return a default strategy
            logger.warning("Failed to parse strategy response, using default strategy")
            strategy = self._get_default_strategy()
        
        # Validate and fix the strategy
        return self._validate_strategy(strategy, platform_performance)

    def _create_strategy_prompt(
        self, 
        keywords: List[str], 
        location: str,
        platform_performance: Optional[Dict[str, Dict[str, float]]] = None
    ) -> str:
        """
        Create prompt for search strategy.
        
        Args:
            keywords: List of search keywords
            location: Job location
            platform_performance: Dictionary of platform performance metrics
            
        Returns:
            Prompt string
        """
        performance_info = ""
        if platform_performance:
            performance_info = "Platform performance metrics:\n"
            for platform, metrics in platform_performance.items():
                performance_info += f"- {platform}: Success rate: {metrics.get('success_rate', 0):.2f}, "
                performance_info += f"Avg results: {metrics.get('avg_results', 0):.1f}, "
                performance_info += f"Avg time: {metrics.get('avg_time', 0):.1f}s\n"
        
        return f"""
        Create a targeted job search strategy using the provided keywords and location.

        Context:
            1. Focus only on closely related technical skills, modern job titles, and industry-specific terminology that are commonly used in job descriptions.
            2. Avoid generic terms or excessive keyword expansion.
        Use available performance metrics to:
            1. Recommend top 3–5 platforms in priority order.
            2. Suggest effective job search filters (e.g., recency, job type).
            3. Propose concise keyword variations that can enhance search accuracy.
            4. Highlight any special considerations based on the location and industry.
        Input: Keywords: {keywords} Location: {location} Platform metrics: {performance_info}.
        Output: Return a well-formatted JSON with these keys:
                platforms: [ranked list of platforms]
                filters: object with filter criteria
                keywordVariations: [short, meaningful variations]
                specialConsiderations: [specific notes for better targeting]
        Return only a valid, minified JSON object.
        Do not include explanations, markdown formatting, code blocks, or escaped characters.
        Do not wrap the JSON in quotes. Output must be directly parsable by json.loads().
        Your output must begin with "{" and end with "}".
        """

    def _get_default_strategy(self) -> Dict[str, Any]:
        """
        Get default search strategy.
        
        Returns:
            Default strategy dictionary
        """
        return {
            "platforms": ["linkedin", "indeed", "glassdoor"],
            "filters": {"datePosted": "past week"},
            "keywordVariations": [],
            "specialConsiderations": []
        }

    def _validate_strategy(
        self, 
        strategy: Dict[str, Any],
        platform_performance: Optional[Dict[str, Dict[str, float]]] = None
    ) -> Dict[str, Any]:
        """
        Validate and fix search strategy.
        
        Args:
            strategy: Strategy dictionary
            platform_performance: Dictionary of platform performance metrics
            
        Returns:
            Validated strategy dictionary
        """
        # Ensure required fields exist
        if "platforms" not in strategy:
            strategy["platforms"] = []
        if "filters" not in strategy:
            strategy["filters"] = {}
        if "keywordVariations" not in strategy:
            strategy["keywordVariations"] = []
        if "specialConsiderations" not in strategy:
            strategy["specialConsiderations"] = []
        
        # Validate platforms
        valid_platforms = [p for p in strategy["platforms"] if p.lower() in [ap.lower() for ap in self.available_platforms]]
        
        # If no valid platforms or too few, add default platforms
        if len(valid_platforms) < 3:
            # Use performance metrics to prioritize if available
            if platform_performance:
                # Sort platforms by success rate * avg_results
                sorted_platforms = sorted(
                    platform_performance.items(),
                    key=lambda x: x[1].get('success_rate', 0) * x[1].get('avg_results', 0),
                    reverse=True
                )
                # Add top performing platforms that aren't already included
                for platform, _ in sorted_platforms:
                    if platform in self.available_platforms and platform not in valid_platforms:
                        valid_platforms.append(platform)
                        if len(valid_platforms) >= 3:
                            break
            
            # If still not enough, add default platforms
            default_platforms = ["linkedin", "indeed", "glassdoor"]
            for platform in default_platforms:
                if platform not in valid_platforms:
                    valid_platforms.append(platform)
                    if len(valid_platforms) >= 3:
                        break
        
        strategy["platforms"] = valid_platforms[:5]  # Limit to 5 platforms
        
        # Convert to the format expected by the API
        formatted_strategy = {"platforms": []}
        for i, platform in enumerate(strategy["platforms"], 1):
            formatted_strategy["platforms"].append(platform)
            formatted_strategy[platform] = {
                "priority": i,
                "keywords": strategy.get("keywordVariations", [])[:5] or [""],  # Use empty string if no variations
                "filters": strategy.get("filters", {})
            }
            
            # Ensure filters is a dictionary
            if not isinstance(formatted_strategy[platform]["filters"], dict):
                formatted_strategy[platform]["filters"] = {}
                
            # Add date_posted filter if not present
            if "date_posted" not in formatted_strategy[platform]["filters"]:
                formatted_strategy[platform]["filters"]["date_posted"] = "past_week"
        
        return formatted_strategy