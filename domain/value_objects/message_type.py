from enum import Enum, auto

class MessageType(Enum):
    """
    Enum representing the type of a message.
    
    This enum is used to distinguish between different types of messages
    in a conversation.
    """
    USER = auto()               # Message from a user
    ASSISTANT = auto()          # Message from the assistant
    FUNCTION_CALL = auto()      # Message representing a function call
    FUNCTION_RESULT = auto()    # Message representing a function result
    
    @classmethod
    def from_string(cls, value: str) -> 'MessageType':
        """
        Convert a string to a MessageType.
        
        Args:
            value: The string value to convert
            
        Returns:
            The corresponding MessageType
            
        Raises:
            ValueError: If the string is not a valid MessageType
        """
        value = value.upper()
        if value == "USER":
            return cls.USER
        elif value == "ASSISTANT":
            return cls.ASSISTANT
        elif value == "FUNCTION_CALL":
            return cls.FUNCTION_CALL
        elif value == "FUNCTION_RESULT":
            return cls.FUNCTION_RESULT
        else:
            raise ValueError(f"Invalid MessageType: {value}")
    
    def __str__(self) -> str:
        """
        Convert the MessageType to a string.
        
        Returns:
            The string representation of the MessageType
        """
        if self == self.USER:
            return "user"
        elif self == self.ASSISTANT:
            return "assistant"
        elif self == self.FUNCTION_CALL:
            return "function_call"
        elif self == self.FUNCTION_RESULT:
            return "function_result"
        else:
            return "unknown"