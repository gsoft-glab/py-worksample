from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

###################################################################################################
# Conversation Models
###################################################################################################

class CreateConversationRequest(BaseModel):
    """Request model for creating a conversation"""
    title: str = Field(default="New Conversation", description="The title of the conversation")
    owner_id: Optional[str] = Field(default=None, description="The ID of the owner (for private conversations)")

class AddMessageRequest(BaseModel):
    """Request model for adding a message to a conversation"""
    content: str = Field(description="The content of the message")
    owner_id: Optional[str] = Field(default=None, description="The ID of the owner (for private conversations)")

###################################################################################################
# Function Models
####################################################################################################

class CallFunctionRequest(BaseModel):
    """Request model for calling a function"""
    name: str = Field(description="The name of the function to call")
    arguments: Dict[str, Any] = Field(default={}, description="The arguments to pass to the function")