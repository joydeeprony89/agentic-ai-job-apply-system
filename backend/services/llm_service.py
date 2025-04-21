"""
LLM Service for handling interactions with language model providers.
Currently supports Groq API.
"""
from typing import Dict, Any, List, Optional
import httpx
from tenacity import retry, wait_exponential, stop_after_attempt
import json
import re

from core.config import settings
from core.logging import get_logger

# Get logger
logger = get_logger(__name__)

class LLMServiceError(Exception):
    """Base exception for LLM service errors."""
    pass

class APIConnectionError(LLMServiceError):
    """Exception raised when connection to LLM API fails."""
    pass

class APIResponseError(LLMServiceError):
    """Exception raised when LLM API returns an error."""
    pass

class ResponseParsingError(LLMServiceError):
    """Exception raised when parsing the LLM API response fails."""
    pass

class GroqService:
    """Service for interacting with Groq API."""
    
    def __init__(self, api_key: str = None):
        """
        Initialize Groq service.
        
        Args:
            api_key: Groq API key. If None, uses the one from settings.
        """
        self.api_key = api_key or settings.GROQ_API_KEY
        self.base_url = settings.GROQ_API_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    @retry(
        wait=wait_exponential(multiplier=1, min=4, max=10),
        stop=stop_after_attempt(3),
        reraise=True
    )
    async def generate_completion(
        self, 
        prompt: str, 
        model: str = None,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> Dict[str, Any]:
        """
        Generate completion using Groq API.
        
        Args:
            prompt: Prompt to send to Groq
            model: Model to use (defaults to settings.DEFAULT_LLM_MODEL)
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
            
        Returns:
            Processed API response
            
        Raises:
            APIConnectionError: If connection to API fails
            APIResponseError: If API returns an error
            ResponseParsingError: If parsing the response fails
        """
        # Use the default model from settings if none is provided
        model = model or settings.DEFAULT_LLM_MODEL
        try:
            # Log the request (without the full prompt for privacy/space reasons)
            prompt_preview = prompt[:100] + "..." if len(prompt) > 100 else prompt
            logger.debug(f"Calling Groq API with model={model}, temp={temperature}, prompt={prompt_preview}")
            
            # Make the API call
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.base_url,
                    headers=self.headers,
                    json={
                        "model": model,
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": temperature,
                        "max_tokens": max_tokens
                    },
                    timeout=30.0  # 30 second timeout
                )
                
                # Parse the response
                response_json = response.json()
                
                # Check for API errors
                if "error" in response_json:
                    error_message = response_json.get("error", {}).get("message", "Unknown Groq API error")
                    logger.error(f"Groq API error with model {model}: {error_message}")
                    
                    # If the error is model-related and we're not already using the fallback model, try the fallback
                    if (model != settings.FALLBACK_LLM_MODEL and 
                        ("model" in error_message.lower() or "not found" in error_message.lower())):
                        logger.info(f"Trying fallback model: {settings.FALLBACK_LLM_MODEL}")
                        return await self.generate_completion(
                            prompt, 
                            model=settings.FALLBACK_LLM_MODEL,
                            temperature=temperature,
                            max_tokens=max_tokens
                        )
                    
                    raise APIResponseError(f"Groq API error: {error_message}")
                
                # Check for expected response structure
                if "choices" not in response_json or not response_json["choices"]:
                    logger.error("Invalid response format from Groq API: missing 'choices'")
                    raise ResponseParsingError("Invalid response format from Groq API: missing 'choices'")
                
                if "message" not in response_json["choices"][0]:
                    logger.error("Invalid response format from Groq API: missing 'message' in choices")
                    raise ResponseParsingError("Invalid response format from Groq API: missing 'message' in choices")
                
                # Return the validated response
                return response_json
                
        except httpx.RequestError as e:
            logger.error(f"Error connecting to Groq API: {str(e)}")
            raise APIConnectionError(f"Error connecting to Groq API: {str(e)}")
        except (KeyError, json.JSONDecodeError) as e:
            logger.error(f"Error parsing Groq API response: {str(e)}")
            raise ResponseParsingError(f"Error parsing Groq API response: {str(e)}")
    
    def extract_text_content(self, response: Dict[str, Any]) -> str:
        """
        Extract text content from Groq API response.
        
        Args:
            response: Groq API response
            
        Returns:
            Text content
            
        Raises:
            ResponseParsingError: If extracting content fails
        """
        try:
            return response["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as e:
            logger.error(f"Error extracting content from Groq API response: {str(e)}")
            raise ResponseParsingError(f"Error extracting content from Groq API response: {str(e)}")
    
    def extract_json_content(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract and parse JSON content from Groq API response.
        
        Args:
            response: Groq API response
            
        Returns:
            Parsed JSON content
            
        Raises:
            ResponseParsingError: If extracting or parsing JSON fails
        """
        try:
            content = self.extract_text_content(response)
            
            # Try to extract JSON from code blocks first
            json_match = re.search(r'```(?:json)?\s*(.*?)\s*```', content, re.DOTALL)
            if json_match:
                content = json_match.group(1)
            else:
                # Try to find JSON object without code block
                json_match = re.search(r'(\{.*\})', content, re.DOTALL)
                if json_match:
                    content = json_match.group(1)
            
            # Parse the JSON
            return json.loads(content)
            
        except (json.JSONDecodeError, AttributeError) as e:
            logger.error(f"Error parsing JSON from Groq API response: {str(e)}")
            raise ResponseParsingError(f"Error parsing JSON from Groq API response: {str(e)}")
    
    def extract_list_content(self, response: Dict[str, Any], delimiter: str = ',') -> List[str]:
        """
        Extract and parse list content from Groq API response.
        
        Args:
            response: Groq API response
            delimiter: Delimiter for splitting the list
            
        Returns:
            List of strings
            
        Raises:
            ResponseParsingError: If extracting or parsing list fails
        """
        try:
            content = self.extract_text_content(response)
            
            # Handle empty content
            if not content or content.isspace():
                return []
                
            # Parse the list
            return [item.strip() for item in content.split(delimiter) if item.strip()]
            
        except Exception as e:
            logger.error(f"Error parsing list from Groq API response: {str(e)}")
            raise ResponseParsingError(f"Error parsing list from Groq API response: {str(e)}")


# Create a singleton instance for global use
groq_service = GroqService()