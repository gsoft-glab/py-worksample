from typing import Dict, Any
import uuid
from domain.services.abstract_function_caller import AbstractFunctionCaller
from domain.entities.function import Function
from domain.entities.function_call import FunctionCall

class FunctionCaller(AbstractFunctionCaller):
    def call_function(self, function: Function, parameters: Dict[str, Any]) -> FunctionCall:
        if not self.validate_parameters(function, parameters):
            function_call = FunctionCall(
                id=f"call_{uuid.uuid4()}",
                function_id=function.id,
                parameters=parameters,
                result={"error": "Invalid parameters"},
                status="failed"
            )
            return function_call
        
        result = self._execute_function(function, parameters)
        
        function_call = FunctionCall(
            id=f"call_{uuid.uuid4()}",
            function_id=function.id,
            parameters=parameters,
            result=result,
            status="completed"
        )
        
        return function_call
    
    def validate_parameters(self, function: Function, parameters: Dict[str, Any]) -> bool:
        return function.validate_parameters(parameters)
    
    def _execute_function(self, function: Function, parameters: Dict[str, Any]) -> Dict[str, Any]:
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