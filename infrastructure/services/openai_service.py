from typing import Dict, Any, List
import random
from domain.services.abstract_ai_service import AbstractAIService
from domain.entities.function import Function

class OpenAIService(AbstractAIService):
    """    
    This class provides a mock implementation of the OpenAI API for
    generating responses and extracting function calls.
    """
    def __init__(self, api_key: str):
        """
        Initialize the service with an API key.
        
        Args:
            api_key: The OpenAI API key
        """
        self.api_key = api_key
    
    def generate_response(self, message_content: str) -> str:
        # In a real implementation, this would call the OpenAI API
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
    
    def extract_function_calls(self, message_content: str, available_functions: List[Function]) -> List[Dict[str, Any]]:
        # In a real implementation, this would use the OpenAI API to extract function calls        
        function_calls = []
        
        if not available_functions:
            return function_calls
        
        # Check if the message mentions any of the available functions
        for function in available_functions:
            if function.name.lower() in message_content.lower():
                # Create a mock function call
                function_call = {
                    "name": function.name,
                    "arguments": {}
                }
                
                # Add mock arguments
                for param in function.parameters:
                    if param.type == "string":
                        function_call["arguments"][param.name] = "sample_value"
                    elif param.type == "number":
                        function_call["arguments"][param.name] = 42
                    elif param.type == "boolean":
                        function_call["arguments"][param.name] = True
                    else:
                        function_call["arguments"][param.name] = None
                
                function_calls.append(function_call)
                break  # Just return the first match for simplicity
        
        return function_calls