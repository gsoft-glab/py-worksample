from fastapi import FastAPI
from api.controllers.conversation_controller import router as conversation_router
from api.controllers.function_controller import router as function_router

def setup_routes(app: FastAPI) -> None:
    app.include_router(conversation_router, prefix="/api")
    app.include_router(function_router, prefix="/api")