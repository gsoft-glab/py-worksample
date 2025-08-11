import uuid
from domain.entities.conversation import Conversation
from domain.entities.message import Message
from domain.repositories.abstract_repository import AbstractRepository
from domain.services.abstract_message_processor import AbstractMessageProcessor
from application.features.conversation.dtos import MessageDTO
from application.exceptions import NotFoundException

class AddMessageUseCase:
    """
    Use case for adding a message to a conversation.
    """
    def __init__(
        self,
        conversation_repository: AbstractRepository[Conversation],
        message_repository: AbstractRepository[Message],
        message_processor: AbstractMessageProcessor
    ):
        self.conversation_repository = conversation_repository
        self.message_repository = message_repository
        self.message_processor = message_processor
    
    def execute(
        self,
        conversation_id: str,
        content: str,
        sender: str = "user"
    ) -> MessageDTO:
        conversation = self.conversation_repository.find_by_id(conversation_id)
        if not conversation:
            raise NotFoundException(f"Conversation with ID {conversation_id} not found")
        
        message = Message(
            id=f"msg_{uuid.uuid4()}",
            content=content,
            sender=sender,
            conversation_id=conversation_id
        )
        self.message_repository.save(message)
        
        conversation.add_message(message)
        self.conversation_repository.save(conversation)
        
        message_dto = MessageDTO.from_entity(message)
        
        if sender == "user":
            # Process the message and generate a response
            response = self.message_processor.process(message)
            if response:
                self.message_repository.save(response)
                conversation.add_message(response)
                self.conversation_repository.save(conversation)
        
        return message_dto