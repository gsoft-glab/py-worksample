from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from domain.entities.conversation import Conversation, PublicConversation
from application.features.conversation.dtos.message_dto import MessageDTO

class ConversationDTO(BaseModel):
    id: str
    title: str
    created_at: datetime = Field(default_factory=datetime.now)
    owner_id: str
    is_public: bool = False
    messages: List[MessageDTO] = []
    
    @classmethod
    def from_entity(cls, conversation):
        """Create from domain entity"""
        is_public = isinstance(conversation, PublicConversation)
            
        return cls(
            id=conversation.id,
            title=conversation.title,
            created_at=conversation.created_at if hasattr(conversation, "created_at") else datetime.now(),
            owner_id=conversation.owner_id,
            is_public=is_public
        )
    
    def to_entity(self):
        """Convert to domain entity"""
        if self.is_public:
            conversation = PublicConversation(
                id=self.id,
                title=self.title,
                owner_id=self.owner_id
            )
        else:
            conversation = Conversation(
                id=self.id,
                title=self.title,
                owner_id=self.owner_id
            )
        
        return conversation