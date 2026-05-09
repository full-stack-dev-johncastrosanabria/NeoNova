"""Conversation Data Transfer Objects."""

from dataclasses import dataclass
from uuid import UUID


@dataclass
class CreateConversationDTO:
    """DTO for creating a conversation."""

    title: str
    user_id: UUID
