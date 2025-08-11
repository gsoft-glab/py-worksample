from typing import Dict, Any, List
import random
from domain.services.abstract_ai_service import AbstractAIService
from domain.entities.function import Function

class OpenAIService(AbstractAIService):
    """    
    This class provides a mock implementation of the OpenAI API for
    generating responses and extracting function calls.
    """
    def __init__(self, api_key: str):
        """
        Initialize the service with an API key.
        
        Args:
            api_key: The OpenAI API key
        """
        self.api_key = api_key
    
    def generate_response(self, message_content: str) -> str:
        # In a real implementation, this would call the OpenAI API
        responses = [
            "I'm an AI assistant. How can I help you?",
            "That's an interesting question. Let me think about it.",
            "I can help you with that. Here's what you need to know...",
            "I'm not sure I understand. Could you please clarify?",
            "Based on my knowledge, I would recommend..."
        ]
        
        if "weather" in message_content.lower():
            return "I don't have real-time weather data, but I can help you find a weather service."
        elif "function" in message_content.lower() or "call" in message_content.lower():
            return "I think you want me to call a function. Let me try to do that."
        else:
            return random.choice(responses)
    
    def extract_function_calls(self, message_content: str, available_functions: List[Function]) -> List[Dict[str, Any]]:
        # In a real implementation, this would use the OpenAI API to extract function calls
        function_calls = []
        
        if not available_functions:
            return function_calls
        
        message_lower = message_content.lower()
        
        # Define function-specific triggers
        function_triggers = {
            "get_weather": [
                "weather", "temperature", "forecast", "rain", "sunny", "cloudy",
                "humidity", "precipitation", "climate", "meteorological"
            ],
            "get_time": [
                "time", "clock", "hour", "minute", "current time", "what time",
                "timezone", "local time", "utc", "gmt"
            ],
            "calculate": [
                "calculate", "compute", "add", "subtract", "multiply", "divide",
                "sum", "difference", "product", "quotient", "math", "calculation",
                "plus", "minus", "times", "divided by", "+", "-", "*", "/"
            ]
        }
        
        # Check for function-specific triggers first
        for function in available_functions:
            function_name = function.name.lower()
            
            # Check if function name is explicitly mentioned
            function_name_mentioned = function_name in message_lower
            
            # Check for function-specific triggers
            trigger_found = function_name_mentioned
            
            # If function has defined triggers, check for them
            if function_name in function_triggers:
                triggers = function_triggers[function_name]
                for trigger in triggers:
                    if trigger in message_lower:
                        trigger_found = True
                        break
            
            if trigger_found:
                # Create a mock function call
                function_call = {
                    "name": function.name,
                    "arguments": {}
                }
                
                # Special handling for calculate function
                if function.name == "calculate":
                    # Extract operation
                    if "add" in message_lower or "plus" in message_lower or "+" in message_lower:
                        function_call["arguments"]["operation"] = "add"
                    elif "subtract" in message_lower or "minus" in message_lower or "-" in message_lower:
                        function_call["arguments"]["operation"] = "subtract"
                    elif "multiply" in message_lower or "times" in message_lower or "*" in message_lower:
                        function_call["arguments"]["operation"] = "multiply"
                    elif "divide" in message_lower or "divided by" in message_lower or "/" in message_lower:
                        function_call["arguments"]["operation"] = "divide"
                    else:
                        function_call["arguments"]["operation"] = "add"  # Default to add
                    
                    # Extract numbers
                    import re
                    numbers = re.findall(r'\d+', message_content)
                    if len(numbers) >= 2:
                        function_call["arguments"]["a"] = int(numbers[0])
                        function_call["arguments"]["b"] = int(numbers[1])
                    else:
                        # Default values
                        function_call["arguments"]["a"] = 1
                        function_call["arguments"]["b"] = 1
                
                # Special handling for get_weather function
                elif function.name == "get_weather":
                    # Try to extract location
                    location = "New York"  # Default location
                    location_patterns = [
                        r"weather (?:in|for|at) ([a-zA-Z\s]+)",
                        r"temperature (?:in|for|at) ([a-zA-Z\s]+)",
                        r"forecast (?:in|for|at) ([a-zA-Z\s]+)"
                    ]
                    
                    for pattern in location_patterns:
                        import re
                        match = re.search(pattern, message_lower)
                        if match:
                            location = match.group(1).strip()
                            break
                            
                    function_call["arguments"]["location"] = location
                
                # Special handling for get_time function
                elif function.name == "get_time":
                    # Try to extract timezone
                    timezone = "UTC"  # Default timezone
                    timezone_patterns = [
                        r"time (?:in|for) ([a-zA-Z\s]+)",
                        r"clock (?:in|for) ([a-zA-Z\s]+)",
                        r"timezone ([a-zA-Z\s]+)"
                    ]
                    
                    for pattern in timezone_patterns:
                        import re
                        match = re.search(pattern, message_lower)
                        if match:
                            timezone = match.group(1).strip()
                            break
                            
                    function_call["arguments"]["timezone"] = timezone
                
                # Generic handling for other functions
                else:
                    for param in function.parameters:
                        if param.type == "string":
                            function_call["arguments"][param.name] = "sample_value"
                        elif param.type == "number":
                            function_call["arguments"][param.name] = 42
                        elif param.type == "boolean":
                            function_call["arguments"][param.name] = True
                        else:
                            function_call["arguments"][param.name] = None
                
                function_calls.append(function_call)
                break  # Just return the first match for simplicity
        
        return function_calls