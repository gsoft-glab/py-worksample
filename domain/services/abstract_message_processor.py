from typing import Optional
from abc import ABC, abstractmethod
from domain.entities.message import Message

class AbstractMessageProcessor(ABC):
    """
    Abstract interface for processing messages and generating responses.
    """
    @abstractmethod
    def process(self, message: Message) -> Optional[Message]:
        """
        Process a message and generate a response.
        
        Args:
            message: The message to process
            
        Returns:
            A response message if applicable, None otherwise
        """
        pass