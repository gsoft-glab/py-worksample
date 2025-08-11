import uuid
from domain.entities.conversation import Conversation, PublicConversation
from domain.repositories.abstract_repository import AbstractRepository
from application.features.conversation.dtos import ConversationDTO

class CreateConversationUseCase:
    """
    Use case for creating a new conversation.
    """
    def __init__(self, repository: AbstractRepository[Conversation]):
        self.repository = repository
    
    def execute(self, title: str, owner_id: str, is_public: bool = False) -> ConversationDTO:
        conversation_id = f"conv_{uuid.uuid4()}"
        
        if is_public:
            conversation = PublicConversation(
                id=conversation_id,
                title=title,
                owner_id=owner_id
            )
        else:
            conversation = Conversation(
                id=conversation_id,
                title=title,
                owner_id=owner_id
            )
        
        self.repository.save(conversation)
        
        conversation_dto = ConversationDTO.from_entity(conversation)
        
        return conversation_dto