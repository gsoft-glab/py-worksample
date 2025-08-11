from typing import List
from pydantic import BaseModel
from domain.value_objects.function_parameter import FunctionParameter
from domain.entities.function import Function

class FunctionParameterDTO(BaseModel):
    name: str
    type: str
    description: str
    required: bool = False
    
    @classmethod
    def from_entity(cls, parameter: FunctionParameter):
        """Create from domain entity"""
        return cls(
            name=parameter.name,
            type=parameter.type,
            description=parameter.description,
            required=parameter.required
        )
    
    def to_entity(self) -> FunctionParameter:
        """Convert to domain entity"""
        return FunctionParameter(
            name=self.name,
            type=self.type,
            description=self.description,
            required=self.required
        )


class FunctionDTO(BaseModel):
    id: str
    name: str
    description: str
    parameters: List[FunctionParameterDTO]
    
    @classmethod
    def from_entity(cls, function: Function):
        """Create from domain entity"""
        parameters = [FunctionParameterDTO.from_entity(param) for param in function.parameters]
        
        return cls(
            id=function.id,
            name=function.name,
            description=function.description,
            parameters=parameters
        )
    
    def to_entity(self) -> Function:
        """Convert to domain entity"""
        parameters = [param.to_entity() for param in self.parameters]
        
        return Function(
            id=self.id,
            name=self.name,
            description=self.description,
            parameters=parameters
        )