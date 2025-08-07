from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field

# Request Models
class RegisterFunctionRequest(BaseModel):
    """Request model for registering a function"""
    name: str = Field(description="The name of the function")
    description: str = Field(description="The description of the function")
    parameters: List[Dict[str, Any]] = Field(default=[], description="The parameters of the function")

class CallFunctionRequest(BaseModel):
    """Request model for calling a function"""
    name: str = Field(description="The name of the function to call")
    arguments: Dict[str, Any] = Field(default={}, description="The arguments to pass to the function")
    conversation_id: str = Field(description="The ID of the conversation")