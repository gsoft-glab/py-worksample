from typing import List, Dict, Any, Optional
import uuid
from domain.entities.function import Function
from domain.value_objects.function_parameter import FunctionParameter

class FunctionRegistry:
    """
    Registry of available functions.
    
    This class provides a hardcoded list of available functions that match
    the implementations in the FunctionCaller class. This is a deliberate
    violation of the Open/Closed Principle, as we want to control the
    available functions in the code rather than allowing dynamic registration.
    """
    
    @staticmethod
    def get_available_functions() -> List[Function]:
        """
        Get a list of available functions.
        
        Returns:
            A list of Function entities
        """
        return [
            Function(
                id=f"func_{uuid.uuid4()}",
                name="get_weather",
                description="Get the weather for a location",
                parameters=[
                    FunctionParameter(
                        name="location",
                        type="string",
                        description="The location to get weather for",
                        required=False
                    )
                ]
            ),
            Function(
                id=f"func_{uuid.uuid4()}",
                name="get_time",
                description="Get the current time",
                parameters=[
                    FunctionParameter(
                        name="timezone",
                        type="string",
                        description="The timezone to get time for",
                        required=False
                    )
                ]
            ),
            Function(
                id=f"func_{uuid.uuid4()}",
                name="calculate",
                description="Perform a calculation",
                parameters=[
                    FunctionParameter(
                        name="operation",
                        type="string",
                        description="The operation to perform (add, subtract, multiply, divide)",
                        required=False
                    ),
                    FunctionParameter(
                        name="a",
                        type="number",
                        description="The first number",
                        required=False
                    ),
                    FunctionParameter(
                        name="b",
                        type="number",
                        description="The second number",
                        required=False
                    )
                ]
            )
        ]
    
    @staticmethod
    def get_function_by_name(name: str) -> Optional[Function]:
        """
        Get a function by name.
        
        Args:
            name: The name of the function
            
        Returns:
            The function if found, None otherwise
        """
        functions = FunctionRegistry.get_available_functions()
        for function in functions:
            if function.name == name:
                return function
        return None