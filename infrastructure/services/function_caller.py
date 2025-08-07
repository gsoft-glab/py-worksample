from typing import Dict, Any
import uuid
from domain.services.abstract_function_caller import AbstractFunctionCaller
from domain.entities.function import Function
from domain.entities.function_call import FunctionCall

class FunctionCaller(AbstractFunctionCaller):
    """
    Implementation of the AbstractFunctionCaller interface.
    
    This class provides a mock implementation for calling functions
    and validating function parameters.
    """
    def call_function(self, function: Function, parameters: Dict[str, Any]) -> FunctionCall:
        """
        Call a function with the given parameters and return the result.
        
        Args:
            function: The function to call
            parameters: The parameters to pass to the function
            
        Returns:
            A FunctionCall object representing the function call
        """
        # Validate parameters
        if not self.validate_parameters(function, parameters):
            function_call = FunctionCall(
                id=f"call_{uuid.uuid4()}",
                function_id=function.id,
                parameters=parameters,
                result={"error": "Invalid parameters"},
                status="failed"
            )
            return function_call
        
        # Mock function execution
        result = self._execute_function(function, parameters)
        
        # Create function call
        function_call = FunctionCall(
            id=f"call_{uuid.uuid4()}",
            function_id=function.id,
            parameters=parameters,
            result=result,
            status="completed"
        )
        
        return function_call
    
    def validate_parameters(self, function: Function, parameters: Dict[str, Any]) -> bool:
        """
        Validate that the parameters match the function's requirements.
        
        Args:
            function: The function to validate parameters for
            parameters: The parameters to validate
            
        Returns:
            True if the parameters are valid, False otherwise
        """
        # Use the function's validate_parameters method
        return function.validate_parameters(parameters)
    
    def _execute_function(self, function: Function, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a function with the given parameters.
        
        Args:
            function: The function to execute
            parameters: The parameters to pass to the function
            
        Returns:
            The result of the function execution
        """
        # Mock implementation for different functions
        if function.name == "get_weather":
            return {
                "temperature": 72,
                "condition": "sunny",
                "location": parameters.get("location", "Unknown")
            }
        elif function.name == "get_time":
            from datetime import datetime
            return {
                "time": datetime.now().isoformat(),
                "timezone": parameters.get("timezone", "UTC")
            }
        elif function.name == "calculate":
            operation = parameters.get("operation", "add")
            a = parameters.get("a", 0)
            b = parameters.get("b", 0)
            
            if operation == "add":
                return {"result": a + b}
            elif operation == "subtract":
                return {"result": a - b}
            elif operation == "multiply":
                return {"result": a * b}
            elif operation == "divide":
                if b == 0:
                    return {"error": "Division by zero"}
                return {"result": a / b}
            else:
                return {"error": f"Unknown operation: {operation}"}
        else:
            return {"error": f"Function not implemented: {function.name}"}