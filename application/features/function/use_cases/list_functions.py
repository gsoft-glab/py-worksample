from typing import List
from domain.entities.function import Function
from domain.repositories.abstract_repository import AbstractRepository
from application.features.function.dtos import FunctionDTO
from application.features.common import Result

class ListFunctionsUseCase:
    """
    Use case for listing all available functions.
    """
    def __init__(self, repository: AbstractRepository[Function]):
        """
        Initialize the use case with a repository.
        
        Args:
            repository: The repository for retrieving functions
        """
        self.repository = repository
    
    def execute(self) -> Result[List[FunctionDTO]]:
        """
        List all available functions.
        
        Returns:
            A Result containing a list of function DTOs if successful
        """
        try:
            functions = self.repository.find_all()
            
            # Convert to DTOs
            function_dtos = [FunctionDTO.from_entity(function) for function in functions]
            
            return Result.success(function_dtos)
        except Exception as e:
            return Result.failure(f"Failed to list functions: {str(e)}")