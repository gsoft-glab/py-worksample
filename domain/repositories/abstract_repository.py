from typing import List, Optional, Generic, TypeVar
from domain.entities.message import Message
from domain.entities.conversation import Conversation
from domain.entities.function import Function

T = TypeVar('T')

class AbstractRepository(Generic[T]):
    """
    Abstract repository interface for storing and retrieving entities.
    """
    def save(self, entity: T) -> None:
        """
        Save an entity.
        
        Args:
            entity: The entity to save
        """
        pass
    
    def find_by_id(self, id: str) -> Optional[T]:
        """
        Find an entity by ID.
        
        Args:
            id: The ID of the entity to find
            
        Returns:
            The entity if found, None otherwise
        """
        pass
    
    def find_all(self) -> List[T]:
        """
        Find all entities.
        
        Returns:
            A list of all entities
        """
        pass
    
    def delete(self, id: str) -> None:
        """
        Delete an entity.
        
        Args:
            id: The ID of the entity to delete
        """
        pass
    
    def find_messages_by_conversation_id(self, conversation_id: str) -> List[Message]:
        """
        Find all messages in a conversation.
        
        Args:
            conversation_id: The ID of the conversation
            
        Returns:
            A list of messages in the conversation
        """
        pass
    
    def find_messages_by_sender(self, sender: str) -> List[Message]:
        """
        Find all messages from a specific sender.
        
        Args:
            sender: The sender of the messages
            
        Returns:
            A list of messages from the sender
        """
        pass
    
    def find_conversations_by_title(self, title: str) -> List[Conversation]:
        """
        Find conversations by title.
        
        Args:
            title: The title to search for
            
        Returns:
            A list of conversations with matching titles
        """
        pass
    
    def find_recent_conversations(self, limit: int = 10) -> List[Conversation]:
        """
        Find recent conversations.
        
        Args:
            limit: The maximum number of conversations to return
            
        Returns:
            A list of recent conversations
        """
        pass
    
    def find_functions_by_name(self, name: str) -> List[Function]:
        """
        Find functions by name.
        
        Args:
            name: The name to search for
            
        Returns:
            A list of functions with matching names
        """
        pass
    
    def find_functions_by_category(self, category: str) -> List[Function]:
        """
        Find functions by category.
        
        Args:
            category: The category to search for
            
        Returns:
            A list of functions in the category
        """
        pass