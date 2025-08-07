from typing import Dict, Any, Optional
from pydantic import BaseModel
from domain.entities.function_call import FunctionCall

class FunctionCallDTO(BaseModel):
    """
    DTO for function calls.
    """
    id: str
    function_id: str
    parameters: Dict[str, Any]
    result: Optional[Dict[str, Any]] = None
    status: str = "pending"
    
    @classmethod
    def from_entity(cls, function_call: FunctionCall):
        """
        Create a DTO from a function call entity.
        
        Args:
            function_call: The function call entity
            
        Returns:
            A new FunctionCallDTO instance
        """
        return cls(
            id=function_call.id,
            function_id=function_call.function_id,
            parameters=function_call.parameters,
            result=function_call.result,
            status=function_call.status
        )
    
    def to_entity(self) -> FunctionCall:
        """
        Convert the DTO to a function call entity.
        
        Returns:
            A new FunctionCall instance
        """
        return FunctionCall(
            id=self.id,
            function_id=self.function_id,
            parameters=self.parameters,
            result=self.result,
            status=self.status
        )