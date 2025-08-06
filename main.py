from fastapi import FastAPI
import uvicorn

# Import from our layered architecture
from infrastructure.api.routes import router as api_router

# Create FastAPI application
app = FastAPI(
    title="Workleap Python API",
    description="A FastAPI application for Workleap",
    version="0.1.0"
)

# Include API routes
app.include_router(api_router)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Hello from Workleap Python API!",
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
