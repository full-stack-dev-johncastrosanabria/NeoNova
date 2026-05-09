"""Message domain entity."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from domain.enums import MessageRole


@dataclass
class Message:
    """Domain entity representing a single message in a conversation."""

    id: UUID
    conversation_id: UUID
    role: MessageRole
    content: str
    metadata_json: Optional[Dict[str, Any]]
    created_at: datetime

    def __post_init__(self) -> None:
        """Validate entity invariants."""
        if not self.content or not self.content.strip():
            raise ValueError("Message content cannot be empty")
        if not isinstance(self.role, MessageRole):
            raise ValueError(
                f"Invalid message role: must be a MessageRole instance, got {type(self.role)}"
            )
