from fastapi import Depends

from domain.entities.conversation import Conversation
from domain.entities.message import Message
from domain.entities.function import Function
from domain.repositories.abstract_repository import AbstractRepository
from domain.services.abstract_message_processor import AbstractMessageProcessor
from domain.services.abstract_function_caller import AbstractFunctionCaller

from infrastructure.repositories.in_memory_repository import InMemoryRepository
from infrastructure.services.message_processor import MessageProcessor
from infrastructure.services.function_caller import FunctionCaller

from application.features.conversation.use_cases.create_conversation import CreateConversationUseCase
from application.features.conversation.use_cases.get_conversation import GetConversationUseCase
from application.features.conversation.use_cases.add_message import AddMessageUseCase
from application.features.function.use_cases.list_functions import ListFunctionsUseCase
from application.features.function.use_cases.call_function import CallFunctionUseCase

###################################################################################################
# Repository dependencies
###################################################################################################

def get_conversation_repository() -> AbstractRepository[Conversation]:
    return InMemoryRepository[Conversation]("conversations")

def get_message_repository() -> AbstractRepository[Message]:
    return InMemoryRepository[Message]("messages")

def get_function_repository() -> AbstractRepository[Function]:
    return InMemoryRepository[Function]("functions")

###################################################################################################
# Service dependencies
###################################################################################################

def get_function_caller() -> AbstractFunctionCaller:
    return FunctionCaller()

def get_message_processor(
    function_caller: AbstractFunctionCaller = Depends(get_function_caller)
) -> AbstractMessageProcessor:
    return MessageProcessor(function_caller)

###################################################################################################
# Conversation use case dependencies
###################################################################################################

def get_create_conversation_use_case(
    repo: AbstractRepository[Conversation] = Depends(get_conversation_repository)
) -> CreateConversationUseCase:
    return CreateConversationUseCase(repo)

def get_get_conversation_use_case(
    conversation_repo: AbstractRepository[Conversation] = Depends(get_conversation_repository),
    message_repo: AbstractRepository[Message] = Depends(get_message_repository)
) -> GetConversationUseCase:
    return GetConversationUseCase(conversation_repo, message_repo)

def get_add_message_use_case(
    conversation_repo: AbstractRepository[Conversation] = Depends(get_conversation_repository),
    message_repo: AbstractRepository[Message] = Depends(get_message_repository),
    message_processor: AbstractMessageProcessor = Depends(get_message_processor)
) -> AddMessageUseCase:
    return AddMessageUseCase(conversation_repo, message_repo, message_processor)

###################################################################################################
# Function use case dependencies
###################################################################################################

def get_list_functions_use_case() -> ListFunctionsUseCase:
    return ListFunctionsUseCase()

def get_call_function_use_case(
    function_caller: AbstractFunctionCaller = Depends(get_function_caller)
) -> CallFunctionUseCase:
    return CallFunctionUseCase(function_caller)