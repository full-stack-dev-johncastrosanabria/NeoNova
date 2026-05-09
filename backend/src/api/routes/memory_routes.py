"""FastAPI route handlers for memory endpoints."""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from api.auth import get_current_user
from api.dependencies import (
    get_create_memory_use_case,
    get_deactivate_memory_use_case,
    get_list_memories_use_case,
)
from api.schemas.memory_schemas import MemoryRequest, MemoryResponse
from application.dtos.memory_dtos import CreateMemoryDTO
from application.use_cases.memory_use_cases import (
    CreateMemoryUseCase,
    DeactivateMemoryUseCase,
    ListMemoriesUseCase,
)
from domain.entities.user import User

router = APIRouter(prefix="/memories", tags=["memories"])


@router.get("/", status_code=200, response_model=List[MemoryResponse])
async def list_memories(
    current_user: User = Depends(get_current_user),
    use_case: ListMemoriesUseCase = Depends(get_list_memories_use_case),
) -> List[MemoryResponse]:
    """List all active memories for the authenticated user.

    Args:
        current_user: The authenticated user from the JWT token.
        use_case: Injected use case for listing memories.

    Returns:
        200 list of MemoryResponse objects sorted by importance and recency.
    """
    memories = await use_case.execute(user_id=current_user.id)
    return [
        MemoryResponse(
            id=memory.id,
            user_id=memory.user_id,
            type=memory.type.value,
            content=memory.content,
            importance=memory.importance.value,
            is_active=memory.is_active,
            source_message_id=memory.source_message_id,
            created_at=memory.created_at,
            updated_at=memory.updated_at,
        )
        for memory in memories
    ]


@router.post("/", status_code=201, response_model=MemoryResponse)
async def create_memory(
    body: MemoryRequest,
    current_user: User = Depends(get_current_user),
    use_case: CreateMemoryUseCase = Depends(get_create_memory_use_case),
) -> MemoryResponse:
    """Create a new memory for the authenticated user.

    Args:
        body: Request body containing type, content, and importance.
        current_user: The authenticated user from the JWT token.
        use_case: Injected use case for memory creation.

    Returns:
        201 MemoryResponse on success.

    Raises:
        HTTPException 400: If the content is empty or type/importance is
            invalid.
    """
    try:
        memory = await use_case.execute(
            CreateMemoryDTO(
                user_id=current_user.id,
                type=body.type,
                content=body.content,
                importance=body.importance,
            )
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return MemoryResponse(
        id=memory.id,
        user_id=memory.user_id,
        type=memory.type.value,
        content=memory.content,
        importance=memory.importance.value,
        is_active=memory.is_active,
        source_message_id=memory.source_message_id,
        created_at=memory.created_at,
        updated_at=memory.updated_at,
    )


@router.delete("/{memory_id}", status_code=200, response_model=MemoryResponse)
async def deactivate_memory(
    memory_id: UUID,
    current_user: User = Depends(get_current_user),
    use_case: DeactivateMemoryUseCase = Depends(
        get_deactivate_memory_use_case
    ),
) -> MemoryResponse:
    """Deactivate a memory owned by the authenticated user.

    Args:
        memory_id: UUID of the memory to deactivate.
        current_user: The authenticated user from the JWT token.
        use_case: Injected use case for memory deactivation.

    Returns:
        200 MemoryResponse with is_active set to False.

    Raises:
        HTTPException 404: If the memory is not found or not owned by the
            user.
    """
    try:
        memory = await use_case.execute(
            memory_id=memory_id, user_id=current_user.id
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return MemoryResponse(
        id=memory.id,
        user_id=memory.user_id,
        type=memory.type.value,
        content=memory.content,
        importance=memory.importance.value,
        is_active=memory.is_active,
        source_message_id=memory.source_message_id,
        created_at=memory.created_at,
        updated_at=memory.updated_at,
    )
