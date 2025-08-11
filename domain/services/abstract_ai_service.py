from typing import Dict, Any, List
from abc import ABC, abstractmethod
from domain.entities.function import Function

class AbstractAIService(ABC):
    """
    Service interface for interacting with AI models.
    """
    @abstractmethod
    def generate_response(self, message_content: str) -> str:
        """
        Generate a response to a message.
        
        Args:
            message_content: The content of the message to respond to
            
        Returns:
            The generated response
        """
        pass
    
    @abstractmethod
    def extract_function_calls(self, message_content: str, available_functions: List[Function]) -> List[Dict[str, Any]]:
        """
        Extract function calls from a message.
        
        Args:
            message_content: The content of the message to extract function calls from
            available_functions: The list of available functions
            
        Returns:
            A list of function calls extracted from the message
        """
        pass