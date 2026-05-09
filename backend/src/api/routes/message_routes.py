"""FastAPI route handlers for message endpoints."""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from api.auth import get_current_user
from api.dependencies import (
    get_list_messages_use_case,
    get_send_message_use_case,
)
from api.schemas.conversation_schemas import MessageRequest, MessageResponse
from application.dtos.message_dtos import SendMessageDTO
from application.use_cases.message_use_cases import (
    ListMessagesUseCase,
    SendMessageUseCase,
)
from domain.entities.user import User

router = APIRouter(prefix="/conversations", tags=["messages"])


@router.post(
    "/{conversation_id}/messages",
    status_code=200,
    response_model=List[MessageResponse],
)
async def send_message(
    conversation_id: UUID,
    body: MessageRequest,
    current_user: User = Depends(get_current_user),
    use_case: SendMessageUseCase = Depends(get_send_message_use_case),
) -> List[MessageResponse]:
    """Send a message in a conversation and receive an AI response.

    Args:
        conversation_id: UUID of the target conversation.
        body: Request body containing the message content.
        current_user: The authenticated user from the JWT token.
        use_case: Injected use case for sending messages.

    Returns:
        200 list of two MessageResponse objects (user + assistant).

    Raises:
        HTTPException 404: If the conversation is not found or not owned by
            the user.
    """
    try:
        user_message, assistant_message = await use_case.execute(
            dto=SendMessageDTO(
                conversation_id=conversation_id,
                content=body.content,
            ),
            user_id=current_user.id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return [
        MessageResponse(
            id=user_message.id,
            conversation_id=user_message.conversation_id,
            role=user_message.role.value,
            content=user_message.content,
            created_at=user_message.created_at,
        ),
        MessageResponse(
            id=assistant_message.id,
            conversation_id=assistant_message.conversation_id,
            role=assistant_message.role.value,
            content=assistant_message.content,
            created_at=assistant_message.created_at,
        ),
    ]


@router.get(
    "/{conversation_id}/messages",
    status_code=200,
    response_model=List[MessageResponse],
)
async def list_messages(
    conversation_id: UUID,
    current_user: User = Depends(get_current_user),
    use_case: ListMessagesUseCase = Depends(get_list_messages_use_case),
) -> List[MessageResponse]:
    """List all messages in a conversation.

    Args:
        conversation_id: UUID of the conversation to query.
        current_user: The authenticated user from the JWT token.
        use_case: Injected use case for listing messages.

    Returns:
        200 list of MessageResponse objects ordered by creation time.

    Raises:
        HTTPException 404: If the conversation is not found or not owned by
            the user.
    """
    try:
        messages = await use_case.execute(
            conversation_id=conversation_id, user_id=current_user.id
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return [
        MessageResponse(
            id=msg.id,
            conversation_id=msg.conversation_id,
            role=msg.role.value,
            content=msg.content,
            created_at=msg.created_at,
        )
        for msg in messages
    ]
