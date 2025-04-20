"""
Middleware for the API.
"""
import time
import logging
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from core.logging import get_logger


# Get access logger
access_logger = get_logger("access")


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log all requests and responses.
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process the request, log it, and pass it to the next middleware.
        
        Args:
            request: The incoming request
            call_next: The next middleware to call
            
        Returns:
            The response from the next middleware
        """
        # Start timer
        start_time = time.time()
        
        # Get request details
        method = request.method
        url = str(request.url)
        client_host = request.client.host if request.client else "unknown"
        
        # Process the request
        try:
            response = await call_next(request)
            
            # Calculate processing time
            process_time = time.time() - start_time
            
            # Log the request
            access_logger.info(
                f"{client_host} - {method} {url} {response.status_code} - {process_time:.4f}s"
            )
            
            return response
        except Exception as e:
            # Log the error
            process_time = time.time() - start_time
            access_logger.error(
                f"{client_host} - {method} {url} ERROR - {process_time:.4f}s - {str(e)}"
            )
            raise


class APIKeyLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log API key usage.
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process the request, log API key usage, and pass it to the next middleware.
        
        Args:
            request: The incoming request
            call_next: The next middleware to call
            
        Returns:
            The response from the next middleware
        """
        # Get API key from header
        api_key = request.headers.get("X-API-Key")
        
        # Process the request
        response = await call_next(request)
        
        # Log API key usage if authentication failed
        if response.status_code == 401 and "X-API-Key" in request.headers:
            access_logger.warning(
                f"Invalid API key used: {api_key[:5]}... from {request.client.host if request.client else 'unknown'}"
            )
        
        return response