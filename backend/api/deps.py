"""
Dependencies for API routes.
"""
from fastapi import Header, HTTPException, status, Depends, Security, Request
from fastapi.security.api_key import APIKeyHeader

from core.config import settings
from core.logging import get_logger

# Get logger
logger = get_logger(__name__)

# Define API Key security scheme
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(request: Request, api_key: str = Security(api_key_header)):
    """
    Verify that the API key in the header matches the configured API key.
    
    Args:
        request: The incoming request
        api_key: API key from the X-API-Key header
        
    Returns:
        The API key if valid
        
    Raises:
        HTTPException: If the API key is missing or invalid
    """
    client_host = request.client.host if request.client else "unknown"
    
    if api_key is None:
        logger.warning(f"API request without API key from {client_host}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="X-API-Key header is missing",
            headers={"WWW-Authenticate": "ApiKey"},
        )
        
    if api_key != settings.API_KEY:
        logger.warning(f"Invalid API key used: {api_key[:5]}... from {client_host}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    
    logger.debug(f"Valid API key used from {client_host}")
    return api_key