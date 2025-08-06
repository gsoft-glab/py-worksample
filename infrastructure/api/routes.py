from fastapi import APIRouter
from typing import  Dict, Any

# Create router
router = APIRouter(
    prefix="/api",
    tags=["api"],
)

# Example endpoint
@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint."""
    return {
        "status": "healthy"
    }