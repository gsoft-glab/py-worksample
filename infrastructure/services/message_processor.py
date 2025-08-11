from typing import Optional, List
import uuid
from domain.entities.message import Message
from domain.entities.function import Function
from domain.services.abstract_message_processor import AbstractMessageProcessor
from domain.services.abstract_function_caller import AbstractFunctionCaller
from infrastructure.services.openai_service import OpenAIService  # Direct import of concrete class - DIP violation!
from infrastructure.services.function_registry import FunctionRegistry  # Direct import of concrete class - OCP violation!

class MessageProcessor(AbstractMessageProcessor):
    """
    Implementation of the MessageProcessor interface that integrates AI service
    and function calling capabilities.
    """
    def __init__(
        self,
        function_caller: AbstractFunctionCaller
    ):
        """
        Initialize the message processor with required services.
        
        Args:
            function_caller: Service for calling functions
        """
        self.ai_service = OpenAIService(api_key="mock-api-key")
        self.function_caller = function_caller
    
    def process(self, message: Message) -> Optional[Message]:
        """
        Process a message and generate a response.
        
        This implementation:
        1. Checks if the message is from a user
        2. Extracts potential function calls from the message
        3. If function calls are detected, executes them
        4. Otherwise, generates a standard AI response
        
        Args:
            message: The message to process
            
        Returns:
            A response message if applicable, None otherwise
        """
        if message.sender != "user":
            return None
        
        # Get available functions from the registry
        available_functions = FunctionRegistry.get_available_functions()
        
        # Try to extract function calls from the message
        function_calls = self.ai_service.extract_function_calls(
            message.content,
            available_functions
        )
        
        # If function calls were detected
        if function_calls:
            function_call = function_calls[0]  # Take the first function call
            function_name = function_call["name"]
            arguments = function_call["arguments"]
            
            # Find the function from the registry
            function = FunctionRegistry.get_function_by_name(function_name)
            
            if function:
                # Call the function
                result = self.function_caller.call_function(function, arguments)
                
                # Create a response message with the function result
                response_content = f"I called the function '{function_name}' and got this result: {result.result}"
            else:
                response_content = f"I couldn't find the function '{function_name}'."
        else:
            # Generate a standard response
            response_content = self.ai_service.generate_response(message.content)
        
        # Create a response message
        response_message = Message(
            id=f"msg_{uuid.uuid4()}",
            content=response_content,
            sender="assistant",
            conversation_id=message.conversation_id
        )
        
        return response_message