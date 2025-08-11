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
        self.conversation_repository = conversation_repository
        self.message_repository = message_repository
    
    def execute(self, conversation_id: str) -> ConversationDTO:
        conversation = self.conversation_repository.find_by_id(conversation_id)
        
        if not conversation:
            raise NotFoundException(f"Conversation with ID {conversation_id} not found")
        
        message_entities = self.message_repository.find_messages_by_conversation_id(conversation_id)
        
        conversation_dto = ConversationDTO.from_entity(conversation)
        message_dtos = [MessageDTO.from_entity(msg) for msg in message_entities]
        
        conversation_dto.messages = message_dtos
        
        return conversation_dto