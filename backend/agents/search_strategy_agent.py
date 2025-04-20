from typing import List, Dict, Any, Optional
import json
import httpx
import re
from tenacity import retry, wait_exponential, stop_after_attempt

from core.config import settings


class SearchStrategyAgent:
    """
    Agent responsible for determining optimal job search strategies.
    """
    def __init__(self, groq_api_key: str = None):
        self.api_key = groq_api_key or settings.GROQ_API_KEY
        self.base_url = "https://api.groq.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.available_platforms = [
            "linkedin", "indeed", "glassdoor", "naukri", "monster", 
            "ziprecruiter", "dice", "stackoverflow"
        ]

    @retry(
        wait=wait_exponential(multiplier=1, min=4, max=10),
        stop=stop_after_attempt(3)
    )
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
        """
        prompt = self._create_strategy_prompt(keywords, location, platform_performance)
        response = await self._call_groq(prompt)
        strategy = self._parse_strategy_response(response)
        
        # Validate and fix the strategy
        return self._validate_strategy(strategy, platform_performance)

    async def _call_groq(self, prompt: str) -> Dict[str, Any]:
        """
        Call Groq API.
        
        Args:
            prompt: Prompt to send to Groq
            
        Returns:
            Groq API response
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.base_url,
                headers=self.headers,
                json={
                    "model": "mixtral-8x7b-32768",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": 2000
                }
            )
            return response.json()

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
        Create an optimal job search strategy for:
        Keywords: {', '.join(keywords)}
        Location: {location}

        {performance_info}

        Available platforms: {', '.join(self.available_platforms)}

        Consider:
        1. Best platforms to search based on keywords and location
        2. Search priority (which platform first) based on performance metrics if available
        3. Filters to apply (e.g., date posted, job type, experience level)
        4. Location-specific considerations
        5. Industry-specific considerations
        6. Keyword variations that might yield better results

        Format: Return as a JSON object with these fields:
        - platforms: list of platforms in priority order (at least 3 if available)
        - filters: object with filter criteria
        - keywordVariations: list of alternative keyword combinations to try
        - specialConsiderations: array of special notes

        Return ONLY the JSON object, no additional text.
        """

    def _parse_strategy_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse Groq API response.
        
        Args:
            response: Groq API response
            
        Returns:
            Parsed strategy dictionary
        """
        try:
            content = response['choices'][0]['message']['content']
            
            # Extract JSON from the response (in case there's additional text)
            json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
            if json_match:
                content = json_match.group(1)
            else:
                # Try to find JSON object without code block
                json_match = re.search(r'(\{.*\})', content, re.DOTALL)
                if json_match:
                    content = json_match.group(1)
            
            return json.loads(content)
        except (KeyError, json.JSONDecodeError, AttributeError) as e:
            print(f"Error parsing strategy response: {e}")
            # Return default strategy
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
        valid_platforms = [p for p in strategy["platforms"] if p in self.available_platforms]
        
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
        
        return strategy