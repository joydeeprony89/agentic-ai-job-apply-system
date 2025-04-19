from typing import List, Dict, Any
import httpx
from tenacity import retry, wait_exponential

class JobAnalysisAgent:
    def __init__(self, groq_api_key: str):
        self.api_key = groq_api_key
        self.base_url = "https://api.groq.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {groq_api_key}",
            "Content-Type": "application/json"
        }

    @retry(wait=wait_exponential(multiplier=1, min=4, max=10))
    async def analyze_keywords(self, keywords: List[str]) -> List[str]:
        prompt = self._create_keyword_analysis_prompt(keywords)
        response = await self._call_groq(prompt)
        return self._parse_keyword_response(response)

    @retry(wait=wait_exponential(multiplier=1, min=4, max=10))
    async def categorize_job(self, description: str) -> Dict[str, Any]:
        prompt = self._create_job_analysis_prompt(description)
        response = await self._call_groq(prompt)
        return self._parse_job_analysis_response(response)

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

    def _create_keyword_analysis_prompt(self, keywords: List[str]) -> str:
        return f"""
        Analyze these job search keywords and suggest related terms:
        Keywords: {', '.join(keywords)}
        Focus on technical skills, job titles, and industry-specific terms.
        Format: Return as a comma-separated list.
        """

    def _create_job_analysis_prompt(self, description: str) -> str:
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

    def _parse_keyword_response(self, response: Dict[str, Any]) -> List[str]:
        content = response['choices'][0]['message']['content']
        return [term.strip() for term in content.split(',')]

    def _parse_job_analysis_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        content = response['choices'][0]['message']['content']
        return content  # Assuming Groq returns properly formatted JSON