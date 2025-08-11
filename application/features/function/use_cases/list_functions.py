from typing import List
from domain.entities.function import Function
from application.features.function.dtos import FunctionDTO
from infrastructure.services.function_registry import FunctionRegistry

class ListFunctionsUseCase:
    """
    Use case for listing all available functions.
    """
    def __init__(self):
        pass
    
    def execute(self) -> List[FunctionDTO]:
        """
        List all available functions.
        
        Returns:
            A list of function DTOs
        """
        # Get functions from the registry
        functions = FunctionRegistry.get_available_functions()
        
        # Convert to DTOs
        function_dtos = [FunctionDTO.from_entity(function) for function in functions]
        
        return function_dtos