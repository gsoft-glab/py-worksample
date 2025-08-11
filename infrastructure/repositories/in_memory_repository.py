from typing import List, Optional, TypeVar, cast
from domain.repositories.abstract_repository import AbstractRepository
from domain.entities.entity import Entity
from domain.entities.message import Message
from domain.entities.conversation import Conversation
from domain.entities.function import Function
from infrastructure.database.in_memory_database import database

T = TypeVar('T', bound=Entity)

class InMemoryRepository(AbstractRepository[T]):
    """
    Implementation of the Repository interface using in-memory storage.
    Stores domain objects directly instead of converting to dictionaries.
    """
    def __init__(self, entity_type: str):
        self.entity_type = entity_type
    
    def save(self, entity: T) -> None:
        if self.entity_type not in database:
            database[self.entity_type] = []
        
        # Check if entity already exists
        for i, item in enumerate(database[self.entity_type]):
            if item.id == entity.id:
                # Update existing entity
                database[self.entity_type][i] = entity
                return
        
        # Add new entity
        database[self.entity_type].append(entity)
    
    def find_by_id(self, id: str) -> Optional[T]:
        if self.entity_type not in database:
            return None
        
        for item in database[self.entity_type]:
            if item.id == id:
                return cast(T, item)
        
        return None
    
    def find_all(self) -> List[T]:
        if self.entity_type not in database:
            return []
        
        return cast(List[T], database[self.entity_type])
    
    def delete(self, id: str) -> None:
        if self.entity_type not in database:
            return
        
        database[self.entity_type] = [item for item in database[self.entity_type] if item.id != id]
    
    def find_messages_by_conversation_id(self, conversation_id: str) -> List[Message]:
        if self.entity_type != "messages":
            return []
        
        if "messages" not in database:
            return []
        
        messages = []
        for message in database["messages"]:
            if isinstance(message, Message) and message.conversation_id == conversation_id:
                messages.append(message)
        
        return messages
    
    def find_messages_by_sender(self, sender: str) -> List[Message]:
        if self.entity_type != "messages":
            return []
        
        if "messages" not in database:
            return []
        
        messages = []
        for message in database["messages"]:
            if isinstance(message, Message) and message.sender == sender:
                messages.append(message)
        
        return messages
    
    def find_conversations_by_title(self, title: str) -> List[Conversation]:
        if self.entity_type != "conversations":
            return []
        
        if "conversations" not in database:
            return []
        
        conversations = []
        for conversation in database["conversations"]:
            if isinstance(conversation, Conversation) and title.lower() in conversation.title.lower():
                conversations.append(conversation)
        
        return conversations
    
    def find_recent_conversations(self, limit: int = 10) -> List[Conversation]:
        if self.entity_type != "conversations":
            return []
        
        if "conversations" not in database:
            return []
        
        # Sort by created_at (descending) and take the first 'limit' items
        # We assume all conversations have a created_at attribute
        sorted_conversations = sorted(
            database["conversations"],
            key=lambda x: getattr(x, "created_at", None),
            reverse=True
        )[:limit]
        
        return sorted_conversations
    
    def find_functions_by_name(self, name: str) -> List[Function]:
        if self.entity_type != "functions":
            return []
        
        if "functions" not in database:
            return []
        
        functions = []
        for function in database["functions"]:
            if isinstance(function, Function) and name.lower() in function.name.lower():
                functions.append(function)
        
        return functions
    
    def find_functions_by_category(self, category: str) -> List[Function]:
        if self.entity_type != "functions":
            return []
        
        if "functions" not in database:
            return []
        
        functions = []
        for function in database["functions"]:
            if isinstance(function, Function) and hasattr(function, "category") and function.category == category:
                functions.append(function)
        
        return functions