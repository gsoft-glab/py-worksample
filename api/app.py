from fastapi import FastAPI
from api.routes import setup_routes
from api.middleware.exception_handler import setup_exception_handlers

def create_app() -> FastAPI:
    app = FastAPI(
        title="Workleap AI Assistant API",
        description="A FastAPI application for an AI assistant with function calling capabilities",
        version="0.1.0"
    )
    
    setup_exception_handlers(app)    
    setup_routes(app)
    
    return app