"""Conversation domain entity."""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Conversation:
    """Domain entity representing a conversation session."""

    id: UUID
    user_id: UUID
    title: str
    created_at: datetime
    updated_at: datetime

    def update_title(self, new_title: str) -> None:
        """Update the conversation title.

        Args:
            new_title: The new title for the conversation.

        Raises:
            ValueError: If new_title is empty.
        """
        if not new_title or not new_title.strip():
            raise ValueError("Title cannot be empty")
        self.title = new_title
        self.updated_at = datetime.utcnow()
