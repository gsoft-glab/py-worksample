from typing import List
from domain.entities.function import Function
from application.features.function.dtos import FunctionDTO
from application.features.common import Result
from infrastructure.services.function_registry import FunctionRegistry

class ListFunctionsUseCase:
    """
    Use case for listing all available functions.
    """
    def __init__(self):
        pass
    
    def execute(self) -> Result[List[FunctionDTO]]:
        """
        List all available functions.
        
        Returns:
            A Result containing a list of function DTOs if successful
        """
        try:
            # Get functions from the registry
            functions = FunctionRegistry.get_available_functions()
            
            # Convert to DTOs
            function_dtos = [FunctionDTO.from_entity(function) for function in functions]
            
            return Result.success(function_dtos)
        except Exception as e:
            return Result.failure(f"Failed to list functions: {str(e)}")