from typing import List, Optional
import uuid
from domain.entities.function import Function
from domain.value_objects.function_parameter import FunctionParameter
from domain.repositories.abstract_repository import AbstractRepository
from application.features.function.dtos import FunctionDTO
from application.features.common import Result

class RegisterFunctionUseCase:
    """
    Use case for registering a new function.
    """
    def __init__(self, repository: AbstractRepository[Function]):
        """
        Initialize the use case with a repository.
        
        Args:
            repository: The repository for storing functions
        """
        self.repository = repository
    
    def execute(
        self,
        name: str,
        description: str,
        parameters_data: List[dict]
    ) -> Result[FunctionDTO]:
        """
        Register a new function.
        
        Args:
            name: The name of the function
            description: The description of the function
            parameters_data: The parameters data for the function
            
        Returns:
            A Result containing the created function DTO if successful
        """
        try:
            if not name:
                return Result.failure("Function name is required")
            
            parameters = []
            for param_data in parameters_data:
                parameter = FunctionParameter(
                    name=param_data.get("name", ""),
                    type=param_data.get("type", "string"),
                    description=param_data.get("description", ""),
                    required=param_data.get("required", False)
                )
                parameters.append(parameter)
            
            function = Function(
                id=f"func_{uuid.uuid4()}",
                name=name,
                description=description,
                parameters=parameters
            )
            
            self.repository.save(function)
            
            # Convert to DTO
            function_dto = FunctionDTO.from_entity(function)
            
            return Result.success(function_dto)
        except Exception as e:
            return Result.failure(f"Failed to register function: {str(e)}")