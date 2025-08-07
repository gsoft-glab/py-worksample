from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from domain.entities.conversation import Conversation, PrivateConversation

class ConversationDTO(BaseModel):
    id: str
    title: str
    created_at: datetime = Field(default_factory=datetime.now)
    owner_id: Optional[str] = None
    messages: List["MessageDTO"] = []
    
    @classmethod
    def from_entity(cls, conversation):
        owner_id = None
        if hasattr(conversation, "owner_id"):
            owner_id = conversation.owner_id
            
        return cls(
            id=conversation.id,
            title=conversation.title,
            created_at=conversation.created_at if hasattr(conversation, "created_at") else datetime.now(),
            owner_id=owner_id
        )
    
    def to_entity(self):
        if self.owner_id:
            conversation = PrivateConversation(
                id=self.id,
                title=self.title,
                owner_id=self.owner_id
            )
        else:
            conversation = Conversation(
                id=self.id,
                title=self.title
            )
        
        return conversation

# Add forward reference for MessageDTO to avoid circular import
from application.features.conversation.dtos.message_dto import MessageDTO
ConversationDTO.update_forward_refs()