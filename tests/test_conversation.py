import pytest
from domain.entities.conversation import Conversation
from domain.entities.message import Message


def test_conversation_should_reject_messages_from_unauthorized_users():
    """
    Test that a conversation correctly rejects messages from users who are not the owner.
    
    This test verifies that the Conversation.add_message method raises a PermissionError
    when a message from an unauthorized user is added to the conversation.
    """
    # This test will be implemented later
    raise NotImplementedError("Test not implemented yet")