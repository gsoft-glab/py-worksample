from typing import Optional
import uuid
import random
from domain.entities.message import Message
from domain.services.abstract_message_processor import AbstractMessageProcessor

class MessageProcessor(AbstractMessageProcessor):
    """
    Implementation of the MessageProcessor interface.
    """
    def __init__(self):
        """
        Initialize the message processor.
        """
        pass
    
    def process(self, message: Message) -> Optional[Message]:
        """
        Process a message and generate a response.
        
        Args:
            message: The message to process
            
        Returns:
            A response message if applicable, None otherwise
        """
        if message.sender != "user":
            return None
        
        # Generate a response
        response_content = self._generate_response(message.content)
        
        # Create a response message
        response_message = Message(
            id=f"msg_{uuid.uuid4()}",
            content=response_content,
            sender="assistant",
            conversation_id=message.conversation_id
        )
        
        return response_message
    
    def _generate_response(self, message_content: str) -> str:
        """
        Generate a response to a message.
        
        Args:
            message_content: The content of the message to respond to
            
        Returns:
            The generated response
        """
        responses = [
            "I'm an AI assistant. How can I help you?",
            "That's an interesting question. Let me think about it.",
            "I can help you with that. Here's what you need to know...",
            "I'm not sure I understand. Could you please clarify?",
            "Based on my knowledge, I would recommend..."
        ]
        
        if "weather" in message_content.lower():
            return "I don't have real-time weather data, but I can help you find a weather service."
        elif "function" in message_content.lower() or "call" in message_content.lower():
            return "I think you want me to call a function. Let me try to do that."
        else:
            return random.choice(responses)