from typing import List, Optional
from domain.entities.conversation import Conversation
from domain.entities.message import Message
from domain.repositories.abstract_repository import AbstractRepository
from application.features.conversation.dtos import ConversationDTO, MessageDTO
from application.features.common import Result

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
    
    def execute(self, conversation_id: str) -> Result[ConversationDTO]:
        """
        Get a conversation by ID along with its messages.
        
        Args:
            conversation_id: The ID of the conversation to retrieve
            
        Returns:
            A Result containing the conversation DTO with messages if successful
        """
        try:
            # Get the conversation
            conversation = self.conversation_repository.find_by_id(conversation_id)
            
            if not conversation:
                return Result.failure("Conversation not found")
            
            # Get messages for the conversation
            message_entities = self.message_repository.find_messages_by_conversation_id(conversation_id)
            
            # Convert to DTOs
            conversation_dto = ConversationDTO.from_entity(conversation)
            message_dtos = [MessageDTO.from_entity(msg) for msg in message_entities]
            
            # Add messages to the conversation DTO
            conversation_dto.messages = message_dtos
            
            return Result.success(conversation_dto)
        except Exception as e:
            return Result.failure(f"Failed to get conversation: {str(e)}")