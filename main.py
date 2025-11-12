"""
Task Manager API - Main Application Entry Point
"""
from fastapi import FastAPI
from src.api.routes import router

app = FastAPI(
    title="Task Manager API",
    description="A simple REST API for managing tasks and todos",
    version="0.1.0"
)

# Include API routes
app.include_router(router, prefix="/api", tags=["tasks"])

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Task Manager API is running",
        "version": "0.1.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
