from fastapi import FastAPI, APIRouter
from api.controllers.conversation_controller import router as conversation_router
from api.controllers.function_controller import router as function_router

# API router for all /api prefixed endpoints
api_router = APIRouter(
    prefix="/api",
    tags=["api"],
)

# Include API-specific controllers in the api_router
api_router.include_router(conversation_router)
api_router.include_router(function_router)

# Create a health router
health_router = APIRouter(tags=["health"])

@health_router.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }

# Create a root router
root_router = APIRouter(tags=["root"])

@root_router.get("/")
async def root():
    return {
        "message": "Welcome to the Workleap AI Assistant API!",
        "description": "This API provides endpoints for an AI assistant with function calling capabilities.",
        "documentation": "/docs"
    }

def setup_routes(app: FastAPI) -> None:
    # Include the API router
    app.include_router(api_router)
    
    # Include the health router directly in the app
    app.include_router(health_router)
    
    # Include the root router separately to keep it at the root path
    app.include_router(root_router)