from typing import Dict, Any
import uuid
from domain.entities.function import Function
from domain.entities.function_call import FunctionCall
from domain.services.abstract_function_caller import AbstractFunctionCaller
from application.features.function.dtos.function_call_dto import FunctionCallDTO
from application.features.common import Result
from infrastructure.services.function_registry import FunctionRegistry

class CallFunctionUseCase:
    """
    Use case for calling a function.
    
    This use case is responsible for:
    1. Finding a function by name from the registry
    2. Calling the function with provided arguments
    3. Returning a DTO with the function call result
    """
    def __init__(
        self,
        function_caller: AbstractFunctionCaller
    ):
        """
        Initialize the use case with services.
        
        Args:
            function_caller: The service for calling functions
        """
        self.function_caller = function_caller
    
    def execute(
        self,
        function_name: str,
        arguments: Dict[str, Any]
    ) -> Result[FunctionCallDTO]:
        """
        Call a function and return a DTO with the result.
        
        Args:
            function_name: The name of the function to call
            arguments: The arguments to pass to the function
            
        Returns:
            A Result containing the function call DTO if successful
        """
        try:
            if not function_name:
                return Result.failure("Function name is required")
            
            # Find the function by name from the registry
            function = FunctionRegistry.get_function_by_name(function_name)
            
            if not function:
                return Result.failure(f"Function '{function_name}' not found")
            
            # Call the function using the function caller service
            function_call = self.function_caller.call_function(function, arguments)
            
            # Convert to DTO
            function_call_dto = FunctionCallDTO.from_entity(function_call)
            
            return Result.success(function_call_dto)
        except Exception as e:
            return Result.failure(f"Failed to call function: {str(e)}")