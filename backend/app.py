"""
Main application entry point for the Agentic AI Job Application System backend.
"""
import logging
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
from fastapi.openapi.models import SecuritySchemeType

from core.config import settings
from core.logging import get_logger
from api.api import api_router
from api.deps import verify_api_key
from api.middleware import LoggingMiddleware, APIKeyLoggingMiddleware

# Get logger
logger = get_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Agentic AI Job Application System API",
    description="""
    API for the Agentic AI Job Application System
    
    ## Authentication
    
    All API endpoints are protected with API key authentication.
    
    To use the API, include the API key in the `X-API-Key` header of your requests:
    
    ```
    X-API-Key: agentic-ai-job-system-api-key-2024
    ```
    
    Requests without a valid API key will receive a 401 Unauthorized response.
    """,
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for simplicity
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Add logging middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(APIKeyLoggingMiddleware)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Log when the application starts."""
    logger.info("Application startup")
    logger.info(f"API Version: {settings.API_V1_STR}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")

@app.on_event("shutdown")
async def shutdown_event():
    """Log when the application shuts down."""
    logger.info("Application shutdown")

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to the Agentic AI Job Application System API",
        "docs": "/docs",
        "version": "0.1.0"
    }

# Health check endpoint
@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "api_version": "0.1.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)