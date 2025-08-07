from fastapi import APIRouter, HTTPException, Depends
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
from api.models.conversation import (
    CreateConversationRequest,
    AddMessageRequest
)
from typing import List

router = APIRouter(prefix="/conversations", tags=["conversations"])


@router.post("/", response_model=ConversationDTO)
async def create_conversation(
    request: CreateConversationRequest,
    use_case: CreateConversationUseCase = Depends(get_create_conversation_use_case)
) -> ConversationDTO:
    result = use_case.execute(request.title, request.owner_id)
    
    if result.is_failure():
        raise HTTPException(status_code=400, detail=result.error)
    
    return result.get_value()


@router.get("/{conversation_id}", response_model=ConversationDTO)
async def get_conversation(
    conversation_id: str,
    use_case: GetConversationUseCase = Depends(get_get_conversation_use_case)
) -> ConversationDTO:
    result = use_case.execute(conversation_id)
    
    if result.is_failure():
        raise HTTPException(status_code=404, detail=result.error)
    
    return result.get_value()


@router.get("/{conversation_id}/messages", response_model=List[MessageDTO])
async def get_conversation_messages(
    conversation_id: str,
    use_case: GetConversationUseCase = Depends(get_get_conversation_use_case)
) -> List[MessageDTO]:
    result = use_case.execute(conversation_id)
    
    if result.is_failure():
        raise HTTPException(status_code=404, detail=result.error)
    
    return result.get_value().messages


@router.post("/{conversation_id}/messages", response_model=MessageDTO)
async def add_message(
    conversation_id: str,
    request: AddMessageRequest,
    use_case: AddMessageUseCase = Depends(get_add_message_use_case)
) -> MessageDTO:
    result = use_case.execute(conversation_id, request.content, request.sender)
    
    if result.is_failure():
        raise HTTPException(status_code=404, detail=result.error)
    
    return result.get_value()