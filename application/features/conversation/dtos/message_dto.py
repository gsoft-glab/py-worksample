from datetime import datetime
from pydantic import BaseModel, Field
from domain.entities.message import Message

class MessageDTO(BaseModel):
    id: str
    content: str
    sender: str
    conversation_id: str
    created_at: datetime = Field(default_factory=datetime.now)
    
    @classmethod
    def from_entity(cls, message: Message):
        """Create from domain entity"""
        return cls(
            id=message.id,
            content=message.content,
            sender=message.sender,
            conversation_id=message.conversation_id,
            created_at=message.created_at
        )
    
    def to_entity(self) -> Message:
        """Convert to domain entity"""
        message = Message(
            id=self.id,
            content=self.content,
            sender=self.sender,
            conversation_id=self.conversation_id
        )
        message.created_at = self.created_at
        return message