from fastapi import APIRouter, Depends
from application.features.conversation.use_cases.create_conversation import CreateConversationUseCase
from application.features.conversation.use_cases.get_conversation import GetConversationUseCase
from application.features.conversation.use_cases.add_message import AddMessageUseCase
from application.features.conversation.dtos.conversation_dto import ConversationDTO
from application.features.conversation.dtos.message_dto import MessageDTO
from api.dependencies import (
    get_create_conversation_use_case,
    get_get_conversation_use_case,
    get_add_message_use_case
)
from api.models.requests import (
    CreateConversationRequest,
    AddMessageRequest
)
from typing import List

router = APIRouter(prefix="/conversations", tags=["conversations"])


@router.post("/", response_model=ConversationDTO, summary="Create a new conversation with the specified title and owner.")
def create_conversation(
    request: CreateConversationRequest,
    use_case: CreateConversationUseCase = Depends(get_create_conversation_use_case)
) -> ConversationDTO:
    return use_case.execute(request.title, request.owner_id)


@router.get("/{conversation_id}", response_model=ConversationDTO, summary="Retrieve a specific conversation by its unique identifier.")
def get_conversation(
    conversation_id: str,
    use_case: GetConversationUseCase = Depends(get_get_conversation_use_case)
) -> ConversationDTO:
    return use_case.execute(conversation_id)


@router.get("/{conversation_id}/messages", response_model=List[MessageDTO], summary="Get all messages belonging to a specific conversation.")
def get_conversation_messages(
    conversation_id: str,
    use_case: GetConversationUseCase = Depends(get_get_conversation_use_case)
) -> List[MessageDTO]:
    conversation = use_case.execute(conversation_id)
    return conversation.messages


@router.post("/{conversation_id}/messages", response_model=List[MessageDTO], summary="Add a new message to an existing conversation.")
def add_message(
    conversation_id: str,
    request: AddMessageRequest,
    use_case: AddMessageUseCase = Depends(get_add_message_use_case)
) -> List[MessageDTO]:
    return use_case.execute(conversation_id, request.content, request.owner_id)