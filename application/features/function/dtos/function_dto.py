from typing import List
from pydantic import BaseModel
from domain.value_objects.function_parameter import FunctionParameter
from domain.entities.function import Function

class FunctionParameterDTO(BaseModel):
    """
    DTO for function parameters.
    """
    name: str
    type: str
    description: str
    required: bool = False
    
    @classmethod
    def from_entity(cls, parameter: FunctionParameter):
        """
        Create a DTO from a parameter entity.
        
        Args:
            parameter: The parameter entity
            
        Returns:
            A new FunctionParameterDTO instance
        """
        return cls(
            name=parameter.name,
            type=parameter.type,
            description=parameter.description,
            required=parameter.required
        )
    
    def to_entity(self) -> FunctionParameter:
        """
        Convert the DTO to a parameter entity.
        
        Returns:
            A new FunctionParameter instance
        """
        return FunctionParameter(
            name=self.name,
            type=self.type,
            description=self.description,
            required=self.required
        )


class FunctionDTO(BaseModel):
    """
    DTO for functions.
    """
    id: str
    name: str
    description: str
    parameters: List[FunctionParameterDTO]
    
    @classmethod
    def from_entity(cls, function: Function):
        """
        Create a DTO from a function entity.
        
        Args:
            function: The function entity
            
        Returns:
            A new FunctionDTO instance
        """
        parameters = [FunctionParameterDTO.from_entity(param) for param in function.parameters]
        
        return cls(
            id=function.id,
            name=function.name,
            description=function.description,
            parameters=parameters
        )
    
    def to_entity(self) -> Function:
        """
        Convert the DTO to a function entity.
        
        Returns:
            A new Function instance
        """
        parameters = [param.to_entity() for param in self.parameters]
        
        return Function(
            id=self.id,
            name=self.name,
            description=self.description,
            parameters=parameters
        )