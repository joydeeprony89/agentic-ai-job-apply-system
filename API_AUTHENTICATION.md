# API Authentication Guide

This document explains how to use the API key authentication system implemented in the Agentic AI Job Application System.

## Overview

The API uses a simple API key authentication mechanism. All API endpoints require a valid API key to be included in the request headers.

## API Key

The default API key is:

```
agentic-ai-job-system-api-key-2024
```

In a production environment, you should generate a secure random key and set it using environment variables.

## Backend Configuration

The API key is configured in the backend's `core/config.py` file:

```python
API_KEY: str = os.getenv("API_KEY", "agentic-ai-job-system-api-key-2024")
```

To change the API key, you can:

1. Set the `API_KEY` environment variable
2. Modify the default value in the config file

## Frontend Configuration

The frontend stores the API key in the `.env` file:

```
REACT_APP_API_KEY=agentic-ai-job-system-api-key-2024
```

The API service automatically includes this key in all requests to the backend.

## Making Authenticated Requests

### Using the Frontend API Service

The frontend includes an API service that automatically adds the API key to all requests:

```javascript
import { jobDiscoveryApi } from '../services/api';

// The API key is automatically included
jobDiscoveryApi.searchJobs(['python', 'developer'], 'San Francisco')
  .then(response => {
    console.log(response.data);
  })
  .catch(error => {
    console.error(error);
  });
```

### Making Direct API Calls

If you need to make API calls directly (e.g., from Postman or curl), include the API key in the `X-API-Key` header:

```
X-API-Key: agentic-ai-job-system-api-key-2024
```

Example curl request:

```bash
curl -X POST "http://localhost:8000/api/v1/agents/job-discovery/search" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: agentic-ai-job-system-api-key-2024" \
  -d '{"keywords": ["python", "developer"], "location": "San Francisco"}'
```

## Security Considerations

This simple API key authentication is suitable for internal APIs or development environments. For production systems with public exposure, consider:

1. Using HTTPS to encrypt all traffic
2. Implementing more robust authentication (e.g., OAuth 2.0, JWT)
3. Regularly rotating API keys
4. Implementing rate limiting
5. Adding IP restrictions if applicable