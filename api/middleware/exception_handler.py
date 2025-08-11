from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from application.exceptions import ApplicationException

def setup_exception_handlers(app: FastAPI) -> None:
    """
    Set up exception handlers for the application
    
    Args:
        app: The FastAPI application
    """
    
    @app.exception_handler(ApplicationException)
    async def application_exception_handler(request: Request, exc: ApplicationException):
        """
        Handle application exceptions and return appropriate HTTP responses
        """
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message},
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """
        Handle general exceptions and return 500 Internal Server Error
        """
        return JSONResponse(
            status_code=500,
            content={"detail": f"Internal server error: {str(exc)}"},
        )