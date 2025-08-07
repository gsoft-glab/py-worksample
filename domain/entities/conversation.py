from typing import List
from domain.entities.message import Message

class Conversation:
    """
    Base conversation class representing a conversation between a user and the assistant.
    """
    def __init__(self, id: str, title: str):
        self.id = id
        self.title = title
        self.messages: List[Message] = []
    
    def add_message(self, message: Message) -> None:
        """
        Add a message to the conversation.
        
        This method has a contract that it will always add the message
        to the conversation without any restrictions.
        """
        self.messages.append(message)
    
    def get_messages(self) -> List[Message]:
        """
        Get all messages in the conversation.
        
        This method has a contract that it will return all messages
        in the conversation without any filtering.
        """
        return self.messages
    
    def get_message_count(self) -> int:
        """
        Get the number of messages in the conversation.
        """
        return len(self.messages)


class PrivateConversation(Conversation):
    """
    A private conversation that belongs to a specific owner and restricts access
    to messages based on the sender.
    """
    def __init__(self, id: str, title: str, owner_id: str):
        super().__init__(id, title)
        self.owner_id = owner_id
    
    def add_message(self, message: Message) -> None:
        """
        Only allows messages from the owner or the assistant to be added.
        """
        if message.sender != self.owner_id and message.sender != "assistant":
            raise PermissionError("Only the owner can add messages to this conversation")
        
        super().add_message(message)
    
    def get_messages(self) -> List[Message]:
        """
        Only returns messages from the owner and the assistant.
        """
        return [msg for msg in self.messages if msg.sender == self.owner_id or msg.sender == "assistant"]