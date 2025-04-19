from typing import List, Dict, Any
import httpx
from tenacity import retry, wait_exponential

class SearchStrategyAgent:
    def __init__(self, groq_api_key: str):
        self.api_key = groq_api_key
        self.base_url = "https://api.groq.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {groq_api_key}",
            "Content-Type": "application/json"
        }

    @retry(wait=wait_exponential(multiplier=1, min=4, max=10))
    async def optimize_search_strategy(
        self, 
        keywords: List[str], 
        location: str
    ) -> Dict[str, Any]:
        prompt = self._create_strategy_prompt(keywords, location)
        response = await self._call_groq(prompt)
        return self._parse_strategy_response(response)

    async def _call_groq(self, prompt: str) -> Dict[str, Any]:
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

    def _create_strategy_prompt(self, keywords: List[str], location: str) -> str:
        return f"""
        Create an optimal job search strategy for:
        Keywords: {', '.join(keywords)}
        Location: {location}

        Consider:
        1. Best platforms to search (LinkedIn, Naukri)
        2. Search priority (which platform first)
        3. Filters to apply
        4. Location-specific considerations
        5. Industry-specific considerations

        Format: Return as a JSON object with these fields:
        - platforms: list of platforms in priority order
        - filters: object with filter criteria
        - specialConsiderations: array of special notes
        """

    def _parse_strategy_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        content = response['choices'][0]['message']['content']
        return content  # Assuming Groq returns properly formatted JSON