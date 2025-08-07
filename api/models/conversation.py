from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

# Request Models
class CreateConversationRequest(BaseModel):
    """Request model for creating a conversation"""
    title: str = Field(default="New Conversation", description="The title of the conversation")
    owner_id: Optional[str] = Field(default=None, description="The ID of the owner (for private conversations)")

class AddMessageRequest(BaseModel):
    """Request model for adding a message to a conversation"""
    content: str = Field(description="The content of the message")
    sender: str = Field(default="user", description="The sender of the message")