from typing import Dict, Any, Optional
import uuid
import json
from datetime import datetime
from domain.entities.function import Function
from domain.entities.function_call import FunctionCall
from domain.entities.message import Message
from domain.repositories.abstract_repository import AbstractRepository
from application.features.function.dtos import FunctionCallDTO
from application.features.common import Result

class CallFunctionUseCase:
    """
    Use case for calling a function.
    """
    def __init__(
        self,
        function_repository: AbstractRepository[Function],
        function_call_repository: AbstractRepository[FunctionCall],
        message_repository: AbstractRepository[Message]
    ):
        """
        Initialize the use case with repositories.
        
        Args:
            function_repository: The repository for retrieving functions
            function_call_repository: The repository for storing function calls
            message_repository: The repository for storing messages
        """
        self.function_repository = function_repository
        self.function_call_repository = function_call_repository
        self.message_repository = message_repository
    
    def execute(
        self,
        function_name: str,
        arguments: Dict[str, Any],
        conversation_id: str
    ) -> Result[FunctionCallDTO]:
        """
        Call a function.
        
        Args:
            function_name: The name of the function to call
            arguments: The arguments to pass to the function
            conversation_id: The ID of the conversation
            
        Returns:
            A Result containing the function call DTO if successful
        """
        try:
            if not function_name:
                return Result.failure("Function name is required")
            
            if not conversation_id:
                return Result.failure("Conversation ID is required")
            
            # Find the function by name
            functions = self.function_repository.find_all()
            function = next((f for f in functions if f.name == function_name), None)
            
            if not function:
                return Result.failure(f"Function '{function_name}' not found")
            
            # Create a function call
            function_call = FunctionCall(
                id=f"call_{uuid.uuid4()}",
                function_id=function.id,
                parameters=arguments,
                result=None,
                status="pending"
            )
            
            # Execute the function (mock implementation)
            result = self._execute_function(function, arguments)
            
            # Update the function call
            function_call.set_result(result)
            
            # Save the function call
            self.function_call_repository.save(function_call)
            
            # Create a message with the function result
            message = Message(
                id=f"msg_{uuid.uuid4()}",
                content=f"Function {function_name} returned: {json.dumps(result)}",
                sender="function",
                conversation_id=conversation_id
            )
            
            # Save the message
            self.message_repository.save(message)
            
            # Convert to DTO
            function_call_dto = FunctionCallDTO.from_entity(function_call)
            
            return Result.success(function_call_dto)
        except Exception as e:
            return Result.failure(f"Failed to call function: {str(e)}")
    
    def _execute_function(self, function: Function, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a function.
        
        Args:
            function: The function to execute
            arguments: The arguments to pass to the function
            
        Returns:
            The result of the function execution
        """
        # Mock implementation
        if function.name == "get_weather":
            return {
                "temperature": 72,
                "condition": "sunny",
                "location": arguments.get("location", "Unknown")
            }
        elif function.name == "get_time":
            return {
                "time": datetime.now().isoformat(),
                "timezone": arguments.get("timezone", "UTC")
            }
        else:
            return {
                "error": "Function not implemented"
            }