# Backend for Agentic AI Job Application System

This directory contains the backend implementation for the Agentic AI Job Application System.

## Structure

- `agents/`: Agent implementations
- `api/`: API endpoints
- `core/`: Core functionality
- `app.py`: Application entry point

## Job Discovery Agent

A real-time job search agent that searches across multiple job platforms using Groq-powered AI.

### Features

- **Real-time job search** across LinkedIn, Indeed, Glassdoor, and Naukri
- **AI-powered search strategy optimization** using Groq
- **Keyword enhancement** to improve search results
- **Job analysis and categorization** of search results
- **Rate limiting** to avoid IP bans from job sites

### Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Install Playwright browsers:
   ```bash
   playwright install
   ```

3. Set up environment variables:
   ```bash
   # Create a .env file with your Groq API key
   echo "GROQ_API_KEY=your_groq_api_key_here" > .env
   ```

4. Run the application:
   ```bash
   uvicorn app:app --reload
   ```

### API Endpoints

#### Search for Jobs

```
POST /api/v1/agents/job-discovery/search
```

Request body:
```json
{
  "keywords": ["python", "developer"],
  "location": "New York"
}
```

Response:
```json
{
  "success": true,
  "count": 15,
  "jobs": [
    {
      "title": "Python Developer",
      "company": "Example Corp",
      "location": "New York, NY",
      "url": "https://example.com/job/123",
      "source": "linkedin",
      "description": "Job description here...",
      "analysis": {
        "required_skills": ["Python", "Django", "SQL"],
        "experience_level": "mid",
        "job_category": "backend"
      }
    }
  ]
}
```

#### Analyze Keywords

```
POST /api/v1/agents/job-discovery/analyze-keywords
```

Request body:
```json
{
  "keywords": ["python", "developer"]
}
```

Response:
```json
{
  "success": true,
  "original_keywords": ["python", "developer"],
  "enhanced_keywords": ["python", "developer", "software engineer", "django", "flask", "backend"]
}
```

#### Optimize Search Strategy

```
POST /api/v1/agents/job-discovery/optimize-strategy
```

Request body:
```json
{
  "keywords": ["python", "developer"],
  "location": "New York"
}
```

Response:
```json
{
  "success": true,
  "original_keywords": ["python", "developer"],
  "enhanced_keywords": ["python", "developer", "software engineer", "django", "flask", "backend"],
  "strategy": {
    "platforms": ["linkedin", "indeed", "glassdoor"],
    "filters": {
      "datePosted": "past week",
      "jobType": "full-time"
    },
    "keywordVariations": [
      ["python developer", "software engineer"],
      ["python", "django", "flask"]
    ],
    "specialConsiderations": [
      "New York has a high concentration of fintech companies looking for Python developers"
    ]
  }
}
```

### How It Works

1. The user submits a job search request with keywords and location
2. The system enhances the keywords using Groq AI
3. The system determines the optimal search strategy based on the keywords and location
4. The system searches for jobs across multiple platforms in real-time
5. The system analyzes and categorizes the job results
6. The system returns the results to the user

No data is stored between searches, making this a privacy-friendly solution.