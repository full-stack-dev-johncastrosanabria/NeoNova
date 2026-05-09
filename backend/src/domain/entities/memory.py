"""Memory domain entity."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from domain.enums import MemoryImportance, MemoryType


@dataclass
class Memory:
    """Domain entity representing a persistent memory about a user."""

    id: UUID
    user_id: UUID
    type: MemoryType
    content: str
    importance: MemoryImportance
    source_message_id: Optional[UUID]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    def __post_init__(self) -> None:
        """Validate entity invariants."""
        if not self.content or not self.content.strip():
            raise ValueError("Memory content cannot be empty")

    def deactivate(self) -> None:
        """Deactivate this memory so it is excluded from future context."""
        self.is_active = False
        self.updated_at = datetime.utcnow()

    def update_importance(self, new_importance: MemoryImportance) -> None:
        """Update the importance level of this memory.

        Args:
            new_importance: The new importance level.
        """
        self.importance = new_importance
        self.updated_at = datetime.utcnow()
