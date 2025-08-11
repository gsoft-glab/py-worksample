from typing import List
from application.features.function.dtos import FunctionDTO
from infrastructure.services.function_registry import FunctionRegistry

class ListFunctionsUseCase:
    """
    Use case for listing all available functions.
    """
    def __init__(self):
        pass
    
    def execute(self) -> List[FunctionDTO]:
        functions = FunctionRegistry.get_available_functions()
        
        function_dtos = [FunctionDTO.from_entity(function) for function in functions]
        
        return function_dtos