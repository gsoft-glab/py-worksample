from typing import Dict, Any
from datetime import datetime
from domain.entities.entity import Entity

class Message(Entity):
    """
    Message entity representing a message in a conversation.
    """
    def __init__(self, id: str, content: str, sender: str, conversation_id: str, owner_id: str = None):
        super().__init__(id)
        self.content = content
        self.sender = sender
        self.conversation_id = conversation_id
        self.owner_id = owner_id
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
            "owner_id": self.owner_id,
            "conversation_id": self.conversation_id,
            "created_at": self.created_at.isoformat()
        })
        
    def process_content(self) -> Dict[str, Any]:
        """
        Processes message content to determine intent and extract relevant information.
        
        Returns:
            A dictionary containing the processed information
        """
        if self.sender == "user":
            message_lower = self.content.lower()
            
            # Function call intent triggers
            function_call_triggers = [
                "call", "function", "run", "execute", "perform", "use", "invoke",
                "calculate", "compute", "weather", "time", "get", "find", "show"
            ]
            
            # Check for function call intent
            is_function_call = False
            for trigger in function_call_triggers:
                if trigger in message_lower:
                    is_function_call = True
                    break
            
            # Check for specific function patterns
            if any(keyword in message_lower for keyword in ["add", "subtract", "multiply", "divide", "plus", "minus", "times", "+", "-", "*", "/"]):
                is_function_call = True
            
            if any(keyword in message_lower for keyword in ["weather", "temperature", "forecast", "rain", "sunny"]):
                is_function_call = True
                
            if any(keyword in message_lower for keyword in ["time", "clock", "hour", "minute", "timezone"]):
                is_function_call = True
            
            return {"intent": "function_call" if is_function_call else "question"}
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