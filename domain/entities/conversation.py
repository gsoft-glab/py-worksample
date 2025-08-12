from typing import List, override
from domain.entities.message import Message
from domain.entities.entity import Entity

class Conversation(Entity):
    """
    Base conversation class representing a private conversation between a specific owner and the assistant.
    By default, conversations are private and restricted to the owner.
    """
    def __init__(self, id: str, title: str, owner_id: str):
        super().__init__(id)
        self.title = title
        self.owner_id = owner_id
        self.messages: List[Message] = []
    
    def add_message(self, message: Message) -> None:
        """
        Add a message to the conversation.
        
        This method has a contract that it will only add messages from the owner
        or the assistant to maintain privacy.
        """
        if message.owner_id != self.owner_id and message.sender != "assistant":
            raise PermissionError("Only the owner can add messages to this conversation")
        
        self.messages.append(message)
    
    def get_messages(self) -> List[Message]:
        """
        Get all messages in the conversation.
        
        This method has a contract that it will only return messages
        from the owner and the assistant to maintain privacy.
        """
        return [msg for msg in self.messages if msg.sender == self.owner_id or msg.sender == "assistant"]
    
    def get_message_count(self) -> int:
        """
        Get the number of messages in the conversation.
        """
        return len(self.messages)


class PublicConversation(Conversation):
    """
    A public conversation that allows messages from any sender and makes all messages visible.
    """
    @override
    def add_message(self, message: Message) -> None:
        """
        Allows messages from any sender to be added.
        """
        # Bypass the permission check in the parent class
        self.messages.append(message)
    
    @override
    def get_messages(self) -> List[Message]:
        """
        Returns all messages without filtering.
        """
        return self.messages