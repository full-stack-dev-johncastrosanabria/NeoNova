"""FastAPI route handlers for conversation endpoints."""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response

from api.auth import get_current_user
from api.dependencies import (
    get_create_conversation_use_case,
    get_delete_conversation_use_case,
    get_list_conversations_use_case,
)
from api.schemas.conversation_schemas import (
    ConversationRequest,
    ConversationResponse,
)
from application.use_cases.conversation_use_cases import (
    CreateConversationUseCase,
    DeleteConversationUseCase,
    ListConversationsUseCase,
)
from domain.entities.user import User

router = APIRouter(prefix="/conversations", tags=["conversations"])


@router.post("/", status_code=201, response_model=ConversationResponse)
async def create_conversation(
    body: ConversationRequest,
    current_user: User = Depends(get_current_user),
    use_case: CreateConversationUseCase = Depends(
        get_create_conversation_use_case
    ),
) -> ConversationResponse:
    """Create a new conversation for the authenticated user.

    Args:
        body: Request body containing the conversation title.
        current_user: The authenticated user from the JWT token.
        use_case: Injected use case for conversation creation.

    Returns:
        201 ConversationResponse on success.

    Raises:
        HTTPException 400: If the title is empty or invalid.
    """
    try:
        conversation = await use_case.execute(
            title=body.title, user_id=current_user.id
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return ConversationResponse(
        id=conversation.id,
        user_id=conversation.user_id,
        title=conversation.title,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
    )


@router.get("/", status_code=200, response_model=List[ConversationResponse])
async def list_conversations(
    current_user: User = Depends(get_current_user),
    use_case: ListConversationsUseCase = Depends(
        get_list_conversations_use_case
    ),
) -> List[ConversationResponse]:
    """List all conversations belonging to the authenticated user.

    Args:
        current_user: The authenticated user from the JWT token.
        use_case: Injected use case for listing conversations.

    Returns:
        200 list of ConversationResponse objects.
    """
    conversations = await use_case.execute(user_id=current_user.id)
    return [
        ConversationResponse(
            id=conv.id,
            user_id=conv.user_id,
            title=conv.title,
            created_at=conv.created_at,
            updated_at=conv.updated_at,
        )
        for conv in conversations
    ]


@router.delete("/{conversation_id}", status_code=204)
async def delete_conversation(
    conversation_id: UUID,
    current_user: User = Depends(get_current_user),
    use_case: DeleteConversationUseCase = Depends(
        get_delete_conversation_use_case
    ),
) -> Response:
    """Delete a conversation owned by the authenticated user.

    Args:
        conversation_id: UUID of the conversation to delete.
        current_user: The authenticated user from the JWT token.
        use_case: Injected use case for conversation deletion.

    Returns:
        204 No Content on success.

    Raises:
        HTTPException 404: If the conversation is not found or not owned by
            the user.
    """
    try:
        await use_case.execute(
            conversation_id=conversation_id, user_id=current_user.id
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return Response(status_code=204)
