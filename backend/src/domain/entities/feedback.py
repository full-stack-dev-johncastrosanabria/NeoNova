"""Feedback domain entity."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class Feedback:
    """Domain entity representing user feedback on an assistant message."""

    id: UUID
    message_id: UUID
    user_id: UUID
    rating: Optional[int]  # 1–5 scale
    comment: Optional[str]
    correction: Optional[str]
    created_at: datetime

    def __post_init__(self) -> None:
        """Validate entity invariants."""
        if self.rating is not None and not (1 <= self.rating <= 5):
            raise ValueError(
                f"Rating must be between 1 and 5, got {self.rating}"
            )
