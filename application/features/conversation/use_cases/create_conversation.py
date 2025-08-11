from typing import Optional
import uuid
from domain.entities.conversation import Conversation, PrivateConversation
from domain.repositories.abstract_repository import AbstractRepository
from application.features.conversation.dtos import ConversationDTO

class CreateConversationUseCase:
    """
    Use case for creating a new conversation.
    """
    def __init__(self, repository: AbstractRepository[Conversation]):
        """
        Initialize the use case with a repository.
        
        Args:
            repository: The repository for storing conversations
        """
        self.repository = repository
    
    def execute(self, title: str, owner_id: Optional[str] = None) -> ConversationDTO:
        """
        Create a new conversation.
        
        Args:
            title: The title of the conversation
            owner_id: The ID of the owner (for private conversations)
            
        Returns:
            The created conversation DTO
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
        
        self.repository.save(conversation)
        
        # Convert to DTO
        conversation_dto = ConversationDTO.from_entity(conversation)
        
        return conversation_dto