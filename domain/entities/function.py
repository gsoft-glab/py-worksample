from typing import List, Dict, Any
from domain.value_objects.function_parameter import FunctionParameter

class Function:
    """
    Function entity representing a callable function in the AI assistant.
    
    This class represents a function that can be called by the AI assistant.
    It includes metadata about the function such as its name, description,
    and parameters.
    """
    def __init__(
        self,
        id: str,
        name: str,
        description: str,
        parameters: List[FunctionParameter]
    ):
        self.id = id
        self.name = name
        self.description = description
        self.parameters = parameters
    
    def validate_parameters(self, provided_params: Dict[str, Any]) -> bool:
        """
        Validate that the provided parameters match the function's requirements.
        
        Args:
            provided_params: The parameters provided for the function call
            
        Returns:
            True if the parameters are valid, False otherwise
        """
        # Check that all required parameters are provided
        for param in self.parameters:
            if param.required and param.name not in provided_params:
                return False
            
            # If parameter is provided, check its type
            if param.name in provided_params:
                value = provided_params[param.name]
                
                # Basic type checking
                if param.type == "string" and not isinstance(value, str):
                    return False
                elif param.type == "number" and not isinstance(value, (int, float)):
                    return False
                elif param.type == "boolean" and not isinstance(value, bool):
                    return False
                elif param.type == "array" and not isinstance(value, list):
                    return False
                elif param.type == "object" and not isinstance(value, dict):
                    return False
        
        return True