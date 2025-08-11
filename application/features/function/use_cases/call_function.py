from typing import Dict, Any
from domain.services.abstract_function_caller import AbstractFunctionCaller
from application.features.function.dtos.function_call_dto import FunctionCallDTO
from application.exceptions import NotFoundException, ValidationException
from infrastructure.services.function_registry import FunctionRegistry

class CallFunctionUseCase:
    """
    Use case for calling a function.
    """
    def __init__(
        self,
        function_caller: AbstractFunctionCaller
    ):
        self.function_caller = function_caller
    
    def execute(
        self,
        function_name: str,
        arguments: Dict[str, Any]
    ) -> FunctionCallDTO:
        if not function_name:
            raise ValidationException("Function name is required")
        
        function = FunctionRegistry.get_function_by_name(function_name)
        
        if not function:
            raise NotFoundException(f"Function '{function_name}' not found")
        
        function_call = self.function_caller.call_function(function, arguments)
        
        function_call_dto = FunctionCallDTO.from_entity(function_call)
        
        return function_call_dto