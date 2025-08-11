from typing import List, Optional
from domain.entities.conversation import Conversation
from domain.entities.message import Message
from domain.repositories.abstract_repository import AbstractRepository
from application.features.conversation.dtos import ConversationDTO, MessageDTO
from application.exceptions import NotFoundException

class GetConversationUseCase:
    """
    Use case for retrieving a conversation with its messages.
    """
    def __init__(
        self,
        conversation_repository: AbstractRepository[Conversation],
        message_repository: AbstractRepository[Message]
    ):
        """
        Initialize the use case with repositories.
        
        Args:
            conversation_repository: Repository for conversations
            message_repository: Repository for messages
        """
        self.conversation_repository = conversation_repository
        self.message_repository = message_repository
    
    def execute(self, conversation_id: str) -> ConversationDTO:
        """
        Get a conversation by ID along with its messages.
        
        Args:
            conversation_id: The ID of the conversation to retrieve
            
        Returns:
            The conversation DTO with messages
            
        Raises:
            NotFoundException: If conversation not found
        """
        # Get the conversation
        conversation = self.conversation_repository.find_by_id(conversation_id)
        
        if not conversation:
            raise NotFoundException(f"Conversation with ID {conversation_id} not found")
        
        # Get messages for the conversation
        message_entities = self.message_repository.find_messages_by_conversation_id(conversation_id)
        
        # Convert to DTOs
        conversation_dto = ConversationDTO.from_entity(conversation)
        message_dtos = [MessageDTO.from_entity(msg) for msg in message_entities]
        
        # Add messages to the conversation DTO
        conversation_dto.messages = message_dtos
        
        return conversation_dto