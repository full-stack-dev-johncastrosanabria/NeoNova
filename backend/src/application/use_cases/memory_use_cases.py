"""Memory use cases for creating, listing, and deactivating memories."""

from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from application.dtos.memory_dtos import CreateMemoryDTO
from application.interfaces.repositories import IMemoryRepository
from application.services.memory_service import MemoryService
from domain.entities.memory import Memory
from domain.enums import MemoryImportance, MemoryType


class CreateMemoryUseCase:
    """Use case for creating a new memory entry."""

    def __init__(self, memory_repo: IMemoryRepository) -> None:
        """Initialise with required dependencies.

        Args:
            memory_repo: Repository for memory persistence.
        """
        self.memory_repo = memory_repo

    async def execute(self, dto: CreateMemoryDTO) -> Memory:
        """Create and persist a new memory.

        Args:
            dto: Data transfer object containing memory details.

        Returns:
            The newly created and persisted Memory entity.

        Raises:
            ValueError: If content is empty, type is invalid, or importance
                is outside the 1–4 range.
        """
        if not dto.content or not dto.content.strip():
            raise ValueError("Memory content cannot be empty")

        try:
            memory_type = MemoryType(dto.type)
        except ValueError as exc:
            valid = [t.value for t in MemoryType]
            raise ValueError(
                f"Invalid memory type '{dto.type}'. Must be one of: {valid}"
            ) from exc

        if dto.importance not in (imp.value for imp in MemoryImportance):
            raise ValueError(
                "Memory importance must be between 1 and 4"
            )
        memory_importance = MemoryImportance(dto.importance)

        now = datetime.utcnow()
        memory = Memory(
            id=uuid4(),
            user_id=dto.user_id,
            type=memory_type,
            content=dto.content,
            importance=memory_importance,
            source_message_id=None,
            is_active=True,
            created_at=now,
            updated_at=now,
        )

        return await self.memory_repo.create(memory)


class ListMemoriesUseCase:
    """Use case for listing active memories for a user."""

    def __init__(self, memory_service: MemoryService) -> None:
        """Initialise with required dependencies.

        Args:
            memory_service: Service for memory retrieval and sorting.
        """
        self.memory_service = memory_service

    async def execute(self, user_id: UUID) -> List[Memory]:
        """Return all active memories for the given user, sorted by importance.

        Args:
            user_id: The UUID of the user whose memories to retrieve.

        Returns:
            A list of active Memory entities sorted by importance and recency.
        """
        return await self.memory_service.get_active_memories(user_id)


class DeactivateMemoryUseCase:
    """Use case for deactivating a memory owned by a user."""

    def __init__(self, memory_repo: IMemoryRepository) -> None:
        """Initialise with required dependencies.

        Args:
            memory_repo: Repository for memory persistence.
        """
        self.memory_repo = memory_repo

    async def execute(self, memory_id: UUID, user_id: UUID) -> Memory:
        """Deactivate a memory, verifying ownership first.

        Args:
            memory_id: The UUID of the memory to deactivate.
            user_id: The UUID of the requesting user.

        Returns:
            The updated Memory entity with is_active set to False.

        Raises:
            ValueError: If the memory does not exist or does not belong to
                the requesting user.
        """
        memory = await self.memory_repo.find_by_id(memory_id)
        if not memory or memory.user_id != user_id:
            raise ValueError("Memory not found")

        memory.deactivate()
        return await self.memory_repo.update(memory)
