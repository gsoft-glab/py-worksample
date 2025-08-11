from typing import Optional
import uuid
from domain.entities.message import Message
from domain.services.abstract_message_processor import AbstractMessageProcessor
from domain.services.abstract_function_caller import AbstractFunctionCaller
from infrastructure.services.openai_service import OpenAIService
from infrastructure.services.function_registry import FunctionRegistry

class MessageProcessor(AbstractMessageProcessor):
    def __init__(
        self,
        function_caller: AbstractFunctionCaller
    ):
        self.ai_service = OpenAIService(api_key="mock-api-key")
        self.function_caller = function_caller
    
    def process(self, message: Message) -> Optional[Message]:
        if message.sender != "user":
            return None
        
        available_functions = FunctionRegistry.get_available_functions()
        
        function_calls = self.ai_service.extract_function_calls(
            message.content,
            available_functions
        )
        
        # If function calls were detected
        if function_calls:
            function_call = function_calls[0]  # Take the first function call
            function_name = function_call["name"]
            arguments = function_call["arguments"]
            
            function = FunctionRegistry.get_function_by_name(function_name)
            
            if function:
                result = self.function_caller.call_function(function, arguments)
                
                # Create a response message with the function result
                response_content = f"I called the function '{function_name}' and got this result: {result.result}"
            else:
                response_content = f"I couldn't find the function '{function_name}'."
        else:
            # Generate a standard response
            response_content = self.ai_service.generate_response(message.content)
        
        response_message = Message(
            id=f"msg_{uuid.uuid4()}",
            content=response_content,
            sender="assistant",
            conversation_id=message.conversation_id
        )
        
        return response_message