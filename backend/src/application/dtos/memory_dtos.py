"""Memory Data Transfer Objects."""

from dataclasses import dataclass
from uuid import UUID


@dataclass
class CreateMemoryDTO:
    """DTO for creating a memory entry."""

    user_id: UUID
    type: str
    content: str
    importance: int
