"""
Configuration settings for the application.
"""
import os
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings.
    """
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Agentic AI Job Application System"
    
    # CORS settings
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        """
        Parse CORS origins from string or list.
        """
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Security settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "development_secret_key")
    
    # LLM settings
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "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")
    DEFAULT_LLM_MODEL: str = os.getenv("DEFAULT_LLM_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct")
    
    # Database settings
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    MONGODB_DB: str = os.getenv("MONGODB_DB", "agentic_ai_job_system")
    
    # API Security
    API_KEY: str = os.getenv("API_KEY", "agentic-ai-job-system-api-key-2024")
    
    class Config:
        """
        Pydantic config.
        """
        case_sensitive = True
        env_file = ".env"


# Create settings instance
settings = Settings()