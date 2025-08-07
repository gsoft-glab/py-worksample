from typing import Dict, Any, List, Optional
import uuid
import json
import random
from datetime import datetime
from domain.entities.message import Message
from domain.entities.conversation import Conversation, PrivateConversation
from domain.entities.function import Function
from domain.entities.function_call import FunctionCall
from domain.value_objects.function_parameter import FunctionParameter
from infrastructure.database.in_memory_database import database

class ConversationManager:
    """
    This class handles conversation management, message processing, and function calling.
    """
    def __init__(self):
        """
        Initialize the conversation manager.
        """
        pass
    
    def create_conversation(self, title: str, owner_id: Optional[str] = None) -> Conversation:
        """
        Create a new conversation.
        
        Args:
            title: The title of the conversation
            owner_id: The ID of the owner (for private conversations)
            
        Returns:
            The created conversation
        """
        conversation_id = f"conv_{uuid.uuid4()}"
        
        if owner_id:
            conversation = PrivateConversation(
                id=conversation_id,
                title=title,
                owner_id=owner_id
            )
        else:
            conversation = Conversation(
                id=conversation_id,
                title=title
            )
        
        # Save to database
        if "conversations" not in database:
            database["conversations"] = []
        
        database["conversations"].append({
            "id": conversation.id,
            "title": conversation.title,
            "created_at": datetime.now().isoformat(),
            "owner_id": owner_id if owner_id else None
        })
        
        return conversation
    
    def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """
        Get a conversation by ID.
        
        Args:
            conversation_id: The ID of the conversation
            
        Returns:
            The conversation if found, None otherwise
        """
        if "conversations" not in database:
            return None
        
        for item in database["conversations"]:
            if item.get("id") == conversation_id:
                if "owner_id" in item and item["owner_id"]:
                    return PrivateConversation(
                        id=item.get("id", ""),
                        title=item.get("title", ""),
                        owner_id=item.get("owner_id", "")
                    )
                else:
                    return Conversation(
                        id=item.get("id", ""),
                        title=item.get("title", "")
                    )
        
        return None
    
    def add_message(self, conversation_id: str, content: str, sender: str) -> Optional[Message]:
        """
        Add a message to a conversation.
        
        Args:
            conversation_id: The ID of the conversation
            content: The content of the message
            sender: The sender of the message
            
        Returns:
            The created message if successful, None otherwise
        """
        conversation = self.get_conversation(conversation_id)
        if not conversation:
            return None
        
        message = Message(
            id=f"msg_{uuid.uuid4()}",
            content=content,
            sender=sender,
            conversation_id=conversation_id
        )
        
        # Save to database
        if "messages" not in database:
            database["messages"] = []
        
        database["messages"].append({
            "id": message.id,
            "content": message.content,
            "sender": message.sender,
            "conversation_id": message.conversation_id,
            "created_at": datetime.now().isoformat()
        })
        
        # Process the message if it's from a user
        if sender == "user":
            self.process_message(message)
        
        return message
    
    def process_message(self, message: Message) -> Optional[Message]:
        """
        Process a message and generate a response.
        
        Args:
            message: The message to process
            
        Returns:
            The response message if successful, None otherwise
        """
        if message.sender != "user":
            return None
        
        # Generate a response
        response_content = self.generate_response(message.content)
        
        # Create a response message
        response_message = Message(
            id=f"msg_{uuid.uuid4()}",
            content=response_content,
            sender="assistant",
            conversation_id=message.conversation_id
        )
        
        # Save to database
        if "messages" not in database:
            database["messages"] = []
        
        database["messages"].append({
            "id": response_message.id,
            "content": response_message.content,
            "sender": response_message.sender,
            "conversation_id": response_message.conversation_id,
            "created_at": datetime.now().isoformat()
        })
        
        # Check for function calls
        function_calls = self.extract_function_calls(message.content)
        if function_calls:
            for function_call in function_calls:
                self.call_function(
                    function_call["name"],
                    function_call["arguments"],
                    message.conversation_id
                )
        
        return response_message
    
    def generate_response(self, message_content: str) -> str:
        """
        Generate a response to a message.
        
        Args:
            message_content: The content of the message to respond to
            
        Returns:
            The generated response
        """
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
    
    def extract_function_calls(self, message_content: str) -> List[Dict[str, Any]]:
        """
        Extract function calls from a message.
        
        Args:
            message_content: The content of the message to extract function calls from
            
        Returns:
            A list of function calls extracted from the message
        """
        function_calls = []
        
        # Get available functions
        available_functions = self.get_available_functions()
        
        if not available_functions:
            return function_calls
        
        # Check if the message mentions any of the available functions
        for function in available_functions:
            if function.name.lower() in message_content.lower():
                # Create a mock function call
                function_call = {
                    "name": function.name,
                    "arguments": {}
                }
                
                # Add mock arguments
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
    
    def get_available_functions(self) -> List[Function]:
        """
        Get available functions.        
        
        Returns:
            A list of available functions
        """
        if "functions" not in database:
            return []
        
        functions = []
        for item in database["functions"]:
            parameters = []
            if "parameters" in item and isinstance(item["parameters"], list):
                for param_data in item["parameters"]:
                    parameter = FunctionParameter(
                        name=param_data.get("name", ""),
                        type=param_data.get("type", "string"),
                        description=param_data.get("description", ""),
                        required=param_data.get("required", False)
                    )
                    parameters.append(parameter)
            
            function = Function(
                id=item.get("id", ""),
                name=item.get("name", ""),
                description=item.get("description", ""),
                parameters=parameters
            )
            functions.append(function)
        
        return functions
    
    def call_function(self, function_name: str, arguments: Dict[str, Any], conversation_id: str) -> Optional[FunctionCall]:
        """
        Call a function.
        
        Args:
            function_name: The name of the function to call
            arguments: The arguments to pass to the function
            conversation_id: The ID of the conversation
            
        Returns:
            The function call if successful, None otherwise
        """
        available_functions = self.get_available_functions()
        
        function = None
        for f in available_functions:
            if f.name == function_name:
                function = f
                break
        
        if not function:
            return None
        
        # Create a function call
        function_call = FunctionCall(
            id=f"call_{uuid.uuid4()}",
            function_id=function.id,
            parameters=arguments,
            result=None,
            status="pending"
        )
        
        # Execute the function (mock implementation)
        result = self.execute_function(function, arguments)
        
        # Update the function call
        function_call.result = result
        function_call.status = "completed"
        
        # Save to database
        if "function_calls" not in database:
            database["function_calls"] = []
        
        database["function_calls"].append({
            "id": function_call.id,
            "function_id": function_call.function_id,
            "parameters": function_call.parameters,
            "result": function_call.result,
            "status": function_call.status,
            "created_at": datetime.now().isoformat()
        })
        
        # Add a message with the function result
        result_message = Message(
            id=f"msg_{uuid.uuid4()}",
            content=f"Function {function_name} returned: {json.dumps(result)}",
            sender="function",
            conversation_id=conversation_id
        )
        
        if "messages" not in database:
            database["messages"] = []
        
        database["messages"].append({
            "id": result_message.id,
            "content": result_message.content,
            "sender": result_message.sender,
            "conversation_id": result_message.conversation_id,
            "created_at": datetime.now().isoformat()
        })
        
        return function_call
    
    def execute_function(self, function: Function, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a function.
        
        Args:
            function: The function to execute
            arguments: The arguments to pass to the function
            
        Returns:
            The result of the function execution
        """
        # Mock implementation
        if function.name == "get_weather":
            return {
                "temperature": 72,
                "condition": "sunny",
                "location": arguments.get("location", "Unknown")
            }
        elif function.name == "get_time":
            return {
                "time": datetime.now().isoformat(),
                "timezone": arguments.get("timezone", "UTC")
            }
        else:
            return {
                "error": "Function not implemented"
            }