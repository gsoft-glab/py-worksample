from typing import Dict, Any, Optional
from pydantic import BaseModel
from domain.entities.function_call import FunctionCall

class FunctionCallDTO(BaseModel):
    id: str
    function_id: str
    parameters: Dict[str, Any]
    result: Optional[Dict[str, Any]] = None
    status: str = "pending"
    
    @classmethod
    def from_entity(cls, function_call: FunctionCall):
        """Create from domain entity"""
        return cls(
            id=function_call.id,
            function_id=function_call.function_id,
            parameters=function_call.parameters,
            result=function_call.result,
            status=function_call.status
        )
    
    def to_entity(self) -> FunctionCall:
        """Convert to domain entity"""
        return FunctionCall(
            id=self.id,
            function_id=self.function_id,
            parameters=self.parameters,
            result=self.result,
            status=self.status
        )