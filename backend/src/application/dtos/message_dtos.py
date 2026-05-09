"""Message Data Transfer Objects."""

from dataclasses import dataclass
from uuid import UUID


@dataclass
class SendMessageDTO:
    """DTO for sending a message."""

    conversation_id: UUID
    content: str
