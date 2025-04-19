"""
Main application entry point for the Agentic AI Job Application System backend.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI app
app = FastAPI(
    title="Agentic AI Job Application System API",
    description="API for the Agentic AI Job Application System",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to the Agentic AI Job Application System API"}

# Health check endpoint
@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)