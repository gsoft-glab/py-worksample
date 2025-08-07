from fastapi import Depends
from typing import Dict, Any, List

from domain.entities.conversation import Conversation
from domain.entities.message import Message
from domain.entities.function import Function
from domain.entities.function_call import FunctionCall
from domain.repositories.abstract_repository import AbstractRepository
from domain.services.abstract_message_processor import AbstractMessageProcessor

from infrastructure.repositories.in_memory_repository import InMemoryRepository
from infrastructure.services.message_processor import MessageProcessor

from application.features.conversation.use_cases.create_conversation import CreateConversationUseCase
from application.features.conversation.use_cases.get_conversation import GetConversationUseCase
from application.features.conversation.use_cases.add_message import AddMessageUseCase
from application.features.function.use_cases.register_function import RegisterFunctionUseCase
from application.features.function.use_cases.list_functions import ListFunctionsUseCase
from application.features.function.use_cases.call_function import CallFunctionUseCase

# Repository dependencies
def get_conversation_repository() -> AbstractRepository[Conversation]:
    """
    Provides a repository for conversations.
    """
    return InMemoryRepository[Conversation]("conversations")

def get_message_repository() -> AbstractRepository[Message]:
    """
    Provides a repository for messages.
    """
    return InMemoryRepository[Message]("messages")

def get_function_repository() -> AbstractRepository[Function]:
    """
    Provides a repository for functions.
    """
    return InMemoryRepository[Function]("functions")

def get_function_call_repository() -> AbstractRepository[FunctionCall]:
    """
    Provides a repository for function calls.
    """
    return InMemoryRepository[FunctionCall]("function_calls")

# Service dependencies
def get_message_processor() -> AbstractMessageProcessor:
    """
    Provides a message processor service.
    """
    return MessageProcessor()

# Use case dependencies
def get_create_conversation_use_case(
    repo: AbstractRepository[Conversation] = Depends(get_conversation_repository)
) -> CreateConversationUseCase:
    """
    Provides a use case for creating conversations.
    """
    return CreateConversationUseCase(repo)

def get_get_conversation_use_case(
    conversation_repo: AbstractRepository[Conversation] = Depends(get_conversation_repository),
    message_repo: AbstractRepository[Message] = Depends(get_message_repository)
) -> GetConversationUseCase:
    """
    Provides a use case for retrieving conversations with their messages.
    """
    return GetConversationUseCase(conversation_repo, message_repo)

def get_add_message_use_case(
    conversation_repo: AbstractRepository[Conversation] = Depends(get_conversation_repository),
    message_repo: AbstractRepository[Message] = Depends(get_message_repository),
    message_processor: AbstractMessageProcessor = Depends(get_message_processor)
) -> AddMessageUseCase:
    """
    Provides a use case for adding messages to conversations.
    """
    return AddMessageUseCase(conversation_repo, message_repo, message_processor)

# Function use case dependencies
def get_register_function_use_case(
    repo: AbstractRepository[Function] = Depends(get_function_repository)
) -> RegisterFunctionUseCase:
    """
    Provides a use case for registering functions.
    """
    return RegisterFunctionUseCase(repo)

def get_list_functions_use_case(
    repo: AbstractRepository[Function] = Depends(get_function_repository)
) -> ListFunctionsUseCase:
    """
    Provides a use case for listing functions.
    """
    return ListFunctionsUseCase(repo)

def get_call_function_use_case(
    function_repo: AbstractRepository[Function] = Depends(get_function_repository),
    function_call_repo: AbstractRepository[FunctionCall] = Depends(get_function_call_repository),
    message_repo: AbstractRepository[Message] = Depends(get_message_repository)
) -> CallFunctionUseCase:
    """
    Provides a use case for calling functions.
    """
    return CallFunctionUseCase(function_repo, function_call_repo, message_repo)