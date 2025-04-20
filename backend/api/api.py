"""
API router configuration.
"""
from fastapi import APIRouter

from api.routes import agent

api_router = APIRouter()
api_router.include_router(agent.router, prefix="/agents", tags=["agents"])