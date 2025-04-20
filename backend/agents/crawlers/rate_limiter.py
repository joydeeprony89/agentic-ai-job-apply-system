"""
Rate limiter for web crawlers.
"""
import time
import asyncio
from typing import Dict, Any, Optional, Callable
import random
from datetime import datetime, timedelta


class RateLimiter:
    """
    Rate limiter for web crawlers to avoid IP bans.
    """
    def __init__(self, requests_per_minute: int = 10):
        self.requests_per_minute = requests_per_minute
        self.interval = 60 / self.requests_per_minute  # seconds per request
        self.last_request_time: Dict[str, float] = {}
        self.backoff_until: Dict[str, datetime] = {}
        self.success_count: Dict[str, int] = {}
        self.failure_count: Dict[str, int] = {}
    
    async def wait(self, domain: str) -> None:
        """
        Wait for the appropriate time before making a request.
        
        Args:
            domain: Domain to rate limit
        """
        # Check if we're in backoff mode
        if domain in self.backoff_until and datetime.now() < self.backoff_until[domain]:
            backoff_seconds = (self.backoff_until[domain] - datetime.now()).total_seconds()
            print(f"In backoff mode for {domain}. Waiting {backoff_seconds:.2f} seconds...")
            await asyncio.sleep(backoff_seconds)
        
        # Calculate wait time
        now = time.time()
        if domain in self.last_request_time:
            elapsed = now - self.last_request_time[domain]
            if elapsed < self.interval:
                # Add jitter to avoid synchronized requests
                jitter = random.uniform(0, 0.5)
                wait_time = self.interval - elapsed + jitter
                await asyncio.sleep(wait_time)
        
        # Update last request time
        self.last_request_time[domain] = time.time()
    
    def record_success(self, domain: str) -> None:
        """
        Record a successful request.
        
        Args:
            domain: Domain of the request
        """
        self.success_count[domain] = self.success_count.get(domain, 0) + 1
        # Reset failure count after 5 consecutive successes
        if self.success_count[domain] >= 5:
            self.failure_count[domain] = 0
    
    def record_failure(self, domain: str, status_code: Optional[int] = None) -> None:
        """
        Record a failed request and implement exponential backoff if needed.
        
        Args:
            domain: Domain of the request
            status_code: HTTP status code of the failure
        """
        self.failure_count[domain] = self.failure_count.get(domain, 0) + 1
        self.success_count[domain] = 0
        
        # Implement exponential backoff for consecutive failures
        if self.failure_count[domain] >= 3:
            # Calculate backoff time: 2^(failure_count-2) minutes, max 60 minutes
            backoff_minutes = min(2 ** (self.failure_count[domain] - 2), 60)
            self.backoff_until[domain] = datetime.now() + timedelta(minutes=backoff_minutes)
            print(f"Too many failures for {domain}. Backing off for {backoff_minutes} minutes.")
        
        # Special handling for specific status codes
        if status_code == 429:  # Too Many Requests
            self.backoff_until[domain] = datetime.now() + timedelta(minutes=15)
            print(f"Rate limited by {domain}. Backing off for 15 minutes.")
        elif status_code in (403, 503):  # Forbidden or Service Unavailable
            self.backoff_until[domain] = datetime.now() + timedelta(minutes=30)
            print(f"Possible ban from {domain}. Backing off for 30 minutes.")


# Create a global rate limiter instance
rate_limiter = RateLimiter()