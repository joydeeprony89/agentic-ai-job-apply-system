/**
 * API service for making requests to the backend
 */
import axios from 'axios';

// API configuration
const API_CONFIG = {
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1',
  apiKey: process.env.REACT_APP_API_KEY || 'agentic-ai-job-system-api-key-2024',
  timeout: 30000, // 30 seconds
};

// Create axios instance
const apiClient = axios.create({
  baseURL: API_CONFIG.baseURL,
  timeout: API_CONFIG.timeout,
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': API_CONFIG.apiKey,
  },
});

// Request interceptor for API calls
apiClient.interceptors.request.use(
  (config) => {
    // Ensure the API key is always included
    config.headers['X-API-Key'] = API_CONFIG.apiKey;
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for API calls
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle API errors
    const errorResponse = {
      status: error.response?.status || 500,
      message: error.response?.data?.detail || 'An unexpected error occurred',
      data: error.response?.data || {},
    };
    
    console.error('API Error:', errorResponse);
    return Promise.reject(errorResponse);
  }
);

// Job Discovery Agent API
const jobDiscoveryApi = {
  /**
   * Search for jobs
   * @param {Array} keywords - List of keywords
   * @param {string} location - Job location
   * @param {Object} options - Additional search options
   * @param {Array} options.platforms - List of platforms to search
   * @param {Array} options.salary_range - Salary range [min, max] in INR
   * @param {string} options.job_type - Job type (full-time, part-time, etc.)
   * @param {string} options.experience_level - Experience level
   * @param {boolean} options.remote_only - Remote only flag
   * @returns {Promise} - Promise with job search results
   */
  searchJobs: (keywords, location, options = {}) => {
    return apiClient.post('/agents/job-discovery/search', {
      keywords,
      location,
      ...options
    });
  },
  
  /**
   * Get job discovery statistics
   * @returns {Promise} - Promise with job discovery statistics
   */
  getStats: () => {
    return apiClient.get('/agents/job-discovery/stats');
  },
  
  /**
   * Analyze keywords
   * @param {Array} keywords - List of keywords to analyze
   * @returns {Promise} - Promise with analyzed keywords
   */
  analyzeKeywords: (keywords) => {
    return apiClient.post('/agents/job-discovery/analyze-keywords', {
      keywords,
    });
  },
  
  /**
   * Optimize search strategy
   * @param {Array} keywords - List of keywords
   * @param {string} location - Job location
   * @returns {Promise} - Promise with optimized search strategy
   */
  optimizeStrategy: (keywords, location) => {
    return apiClient.post('/agents/job-discovery/optimize-strategy', {
      keywords,
      location,
    });
  },
};

export { apiClient, jobDiscoveryApi };