"""Feedback Data Transfer Objects."""

from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class CreateFeedbackDTO:
    """DTO for creating feedback on a message."""

    message_id: UUID
    rating: Optional[int]
    comment: Optional[str]
    correction: Optional[str]
