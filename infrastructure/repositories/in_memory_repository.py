from typing import List, Optional, Any, Dict, TypeVar, cast
from domain.repositories.abstract_repository import AbstractRepository
from domain.entities.message import Message
from domain.entities.conversation import Conversation, PrivateConversation
from domain.entities.function import Function
from domain.value_objects.function_parameter import FunctionParameter
from infrastructure.database.in_memory_database import database

T = TypeVar('T')

class InMemoryRepository(AbstractRepository[T]):
    """
    Implementation of the Repository interface using in-memory storage.
    """
    def __init__(self, entity_type: str):
        """
        Initialize the repository with an entity type.
        
        Args:
            entity_type: The type of entity this repository handles
                         (e.g., "messages", "conversations", "functions")
        """
        self.entity_type = entity_type
    
    def save(self, entity: T) -> None:
        """
        Save an entity to in-memory storage.
        
        Args:
            entity: The entity to save
        """
        if self.entity_type not in database:
            database[self.entity_type] = []
        
        # Convert entity to dict for database
        entity_dict = self._entity_to_dict(entity)
        
        # Check if entity already exists
        for i, item in enumerate(database[self.entity_type]):
            if item.get("id") == entity_dict.get("id"):
                # Update existing entity
                database[self.entity_type][i] = entity_dict
                return
        
        # Add new entity
        database[self.entity_type].append(entity_dict)
    
    def find_by_id(self, id: str) -> Optional[T]:
        """
        Find an entity by ID.
        
        Args:
            id: The ID of the entity to find
            
        Returns:
            The entity if found, None otherwise
        """
        if self.entity_type not in database:
            return None
        
        for item in database[self.entity_type]:
            if item.get("id") == id:
                return self._dict_to_entity(item)
        
        return None
    
    def find_all(self) -> List[T]:
        """
        Find all entities.
        
        Returns:
            A list of all entities
        """
        if self.entity_type not in database:
            return []
        
        return [self._dict_to_entity(item) for item in database[self.entity_type]]
    
    def delete(self, id: str) -> None:
        """
        Delete an entity.
        
        Args:
            id: The ID of the entity to delete
        """
        if self.entity_type not in database:
            return
        
        database[self.entity_type] = [item for item in database[self.entity_type] if item.get("id") != id]
    
    def find_messages_by_conversation_id(self, conversation_id: str) -> List[Message]:
        """
        Find all messages in a conversation.
        
        Args:
            conversation_id: The ID of the conversation
            
        Returns:
            A list of messages in the conversation
        """
        if self.entity_type != "messages":
            return []
        
        if "messages" not in database:
            return []
        
        messages = []
        for item in database["messages"]:
            if item.get("conversation_id") == conversation_id:
                message = self._dict_to_message(item)
                if message:
                    messages.append(message)
        
        return messages
    
    def find_messages_by_sender(self, sender: str) -> List[Message]:
        """
        Find all messages from a specific sender.
        
        Args:
            sender: The sender of the messages
            
        Returns:
            A list of messages from the sender
        """
        if self.entity_type != "messages":
            return []
        
        if "messages" not in database:
            return []
        
        messages = []
        for item in database["messages"]:
            if item.get("sender") == sender:
                message = self._dict_to_message(item)
                if message:
                    messages.append(message)
        
        return messages
    
    def find_conversations_by_title(self, title: str) -> List[Conversation]:
        """
        Find conversations by title.
        
        Args:
            title: The title to search for
            
        Returns:
            A list of conversations with matching titles
        """
        if self.entity_type != "conversations":
            return []
        
        if "conversations" not in database:
            return []
        
        conversations = []
        for item in database["conversations"]:
            if title.lower() in item.get("title", "").lower():
                conversation = self._dict_to_conversation(item)
                if conversation:
                    conversations.append(conversation)
        
        return conversations
    
    def find_recent_conversations(self, limit: int = 10) -> List[Conversation]:
        """
        Find recent conversations.
        
        Args:
            limit: The maximum number of conversations to return
            
        Returns:
            A list of recent conversations
        """
        if self.entity_type != "conversations":
            return []
        
        if "conversations" not in database:
            return []
        
        # Sort by created_at (descending) and take the first 'limit' items
        sorted_items = sorted(
            database["conversations"],
            key=lambda x: x.get("created_at", ""),
            reverse=True
        )[:limit]
        
        conversations = []
        for item in sorted_items:
            conversation = self._dict_to_conversation(item)
            if conversation:
                conversations.append(conversation)
        
        return conversations
    
    def find_functions_by_name(self, name: str) -> List[Function]:
        """
        Find functions by name.
        
        Args:
            name: The name to search for
            
        Returns:
            A list of functions with matching names
        """
        if self.entity_type != "functions":
            return []
        
        if "functions" not in database:
            return []
        
        functions = []
        for item in database["functions"]:
            if name.lower() in item.get("name", "").lower():
                function = self._dict_to_function(item)
                if function:
                    functions.append(function)
        
        return functions
    
    def find_functions_by_category(self, category: str) -> List[Function]:
        """
        Find functions by category.
        
        Args:
            category: The category to search for
            
        Returns:
            A list of functions in the category
        """
        if self.entity_type != "functions":
            return []
        
        if "functions" not in database:
            return []
        
        functions = []
        for item in database["functions"]:
            if item.get("category") == category:
                function = self._dict_to_function(item)
                if function:
                    functions.append(function)
        
        return functions
    
    # Helper methods for entity conversion
    def _entity_to_dict(self, entity: Any) -> Dict[str, Any]:
        """
        Convert an entity to a dictionary for storage.
        
        Args:
            entity: The entity to convert
            
        Returns:
            A dictionary representation of the entity
        """
        if isinstance(entity, Message):
            return {
                "id": entity.id,
                "content": entity.content,
                "sender": entity.sender,
                "conversation_id": entity.conversation_id,
                "created_at": entity.created_at.isoformat()
            }
        elif isinstance(entity, Conversation):
            result = {
                "id": entity.id,
                "title": entity.title,
                "created_at": getattr(entity, "created_at", None)
            }
            
            if isinstance(entity, PrivateConversation):
                result["owner_id"] = entity.owner_id
                
            return result
        elif isinstance(entity, Function):
            return {
                "id": entity.id,
                "name": entity.name,
                "description": entity.description,
                "parameters": [
                    {
                        "name": param.name,
                        "type": param.type,
                        "description": param.description,
                        "required": param.required
                    }
                    for param in entity.parameters
                ]
            }
        else:
            # Generic fallback
            return entity.__dict__ if hasattr(entity, "__dict__") else {}
    
    def _dict_to_entity(self, data: Dict[str, Any]) -> T:
        """
        Convert a dictionary to an entity.
        
        Args:
            data: The dictionary to convert
            
        Returns:
            An entity
        """
        if self.entity_type == "messages":
            return cast(T, self._dict_to_message(data))
        elif self.entity_type == "conversations":
            return cast(T, self._dict_to_conversation(data))
        elif self.entity_type == "functions":
            return cast(T, self._dict_to_function(data))
        else:
            # Generic fallback
            return cast(T, data)
    
    def _dict_to_message(self, data: Dict[str, Any]) -> Optional[Message]:
        """
        Convert a dictionary to a Message entity.
        
        Args:
            data: The dictionary to convert
            
        Returns:
            A Message entity
        """
        if not data:
            return None
        
        message = Message(
            id=data.get("id", ""),
            content=data.get("content", ""),
            sender=data.get("sender", ""),
            conversation_id=data.get("conversation_id", "")
        )
        
        # Set created_at if present
        if "created_at" in data and data["created_at"]:
            from datetime import datetime
            message.created_at = datetime.fromisoformat(data["created_at"])
        
        return message
    
    def _dict_to_conversation(self, data: Dict[str, Any]) -> Optional[Conversation]:
        """
        Convert a dictionary to a Conversation entity.
        
        Args:
            data: The dictionary to convert
            
        Returns:
            A Conversation entity
        """
        if not data:
            return None
        
        if "owner_id" in data and data["owner_id"]:
            conversation = PrivateConversation(
                id=data.get("id", ""),
                title=data.get("title", ""),
                owner_id=data.get("owner_id", "")
            )
        else:
            conversation = Conversation(
                id=data.get("id", ""),
                title=data.get("title", "")
            )
        
        return conversation
    
    def _dict_to_function(self, data: Dict[str, Any]) -> Optional[Function]:
        """
        Convert a dictionary to a Function entity.
        
        Args:
            data: The dictionary to convert
            
        Returns:
            A Function entity
        """
        if not data:
            return None
        
        parameters = []
        if "parameters" in data and isinstance(data["parameters"], list):
            for param_data in data["parameters"]:
                parameter = FunctionParameter(
                    name=param_data.get("name", ""),
                    type=param_data.get("type", "string"),
                    description=param_data.get("description", ""),
                    required=param_data.get("required", False)
                )
                parameters.append(parameter)
        
        return Function(
            id=data.get("id", ""),
            name=data.get("name", ""),
            description=data.get("description", ""),
            parameters=parameters
        )