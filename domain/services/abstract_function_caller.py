from typing import Dict, Any
from abc import ABC, abstractmethod
from domain.entities.function import Function
from domain.entities.function_call import FunctionCall

class AbstractFunctionCaller(ABC):
    """
    Service interface for calling functions.
    """
    @abstractmethod
    def call_function(self, function: Function, parameters: Dict[str, Any]) -> FunctionCall:
        """
        Call a function with the given parameters and return the result.
        
        Args:
            function: The function to call
            parameters: The parameters to pass to the function
            
        Returns:
            A FunctionCall object representing the function call
        """
        pass
    
    @abstractmethod
    def validate_parameters(self, function: Function, parameters: Dict[str, Any]) -> bool:
        """
        Validate that the parameters match the function's requirements.
        
        Args:
            function: The function to validate parameters for
            parameters: The parameters to validate
            
        Returns:
            True if the parameters are valid, False otherwise
        """
        pass