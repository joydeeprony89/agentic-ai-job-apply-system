from typing import Dict, Any
import httpx
from tenacity import retry, wait_exponential

class BaseAgent:
    def __init__(self, groq_api_key: str):
        self.groq_api_key = groq_api_key
        self.base_url = "https://api.groq.com/v1"
        self.headers = {
            "Authorization": f"Bearer {groq_api_key}",
            "Content-Type": "application/json"
        }

    @retry(wait=wait_exponential(multiplier=1, min=4, max=10))
    async def _call_groq(self, prompt: str, model: str = "mixtral-8x7b-32768") -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/completions",
                headers=self.headers,
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": 2000
                }
            )
            return response.json()