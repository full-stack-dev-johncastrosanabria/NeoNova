"""Memory service for managing user memory retrieval and creation."""

from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from application.interfaces.repositories import IMemoryRepository
from domain.entities.memory import Memory
from domain.enums import MemoryImportance, MemoryType


class MemoryService:
    """Service for memory management operations."""

    def __init__(self, memory_repo: IMemoryRepository) -> None:
        """Initialise the service with a memory repository.

        Args:
            memory_repo: The repository used to persist and retrieve memories.
        """
        self.memory_repo = memory_repo

    async def get_active_memories(self, user_id: UUID) -> List[Memory]:
        """Return active memories for a user, sorted by importance then recency.

        Memories are sorted descending by (importance.value, created_at) so
        the most important and most recent memories appear first.

        Args:
            user_id: The UUID of the user whose memories to retrieve.

        Returns:
            A list of active Memory entities sorted by importance and recency.
        """
        memories = await self.memory_repo.find_active_by_user(user_id)
        return sorted(
            memories,
            key=lambda m: (m.importance.value, m.created_at),
            reverse=True,
        )

    async def extract_memory_from_correction(
        self,
        correction: str,
        message_id: UUID,
        user_id: UUID,
    ) -> Memory:
        """Create and persist a CORRECTION memory from user-provided feedback.

        Args:
            correction: The correction text provided by the user.
            message_id: The UUID of the source message being corrected.
            user_id: The UUID of the user who provided the correction.

        Returns:
            The newly created and persisted Memory entity.
        """
        now = datetime.utcnow()
        memory = Memory(
            id=uuid4(),
            user_id=user_id,
            type=MemoryType.CORRECTION,
            content=correction,
            importance=MemoryImportance.HIGH,
            source_message_id=message_id,
            is_active=True,
            created_at=now,
            updated_at=now,
        )
        return await self.memory_repo.create(memory)
