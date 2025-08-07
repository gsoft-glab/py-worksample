from typing import Dict, Any, List
from datetime import datetime

class Message:
    """
    Message entity representing a message in a conversation.
    """
    def __init__(self, id: str, content: str, sender: str, conversation_id: str):
        self.id = id
        self.content = content
        self.sender = sender
        self.conversation_id = conversation_id
        self.created_at = datetime.now()
        
    def save_to_database(self) -> None:
        """
        Directly saves the message to the in-memory database.
        """
        from infrastructure.database.in_memory_database import database
        
        if "messages" not in database:
            database["messages"] = []
            
        database["messages"].append({
            "id": self.id,
            "content": self.content,
            "sender": self.sender,
            "conversation_id": self.conversation_id,
            "created_at": self.created_at.isoformat()
        })
        
    def process_content(self) -> Dict[str, Any]:
        """
        Processes message content.
        """
        if self.sender == "user":
            # Extract intent from user message
            return {"intent": "function_call" if "call" in self.content.lower() else "question"}
        else:
            return {"type": "response"}
            
    def format_for_display(self) -> Dict[str, Any]:
        """
        Formats message for UI display.
        """
        return {
            "id": self.id,
            "content": self.content,
            "sender": self.sender,
            "timestamp": self.created_at.isoformat(),
            "is_read": True
        }