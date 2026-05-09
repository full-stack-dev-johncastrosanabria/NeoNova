"""User domain entity."""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class User:
    """Domain entity representing a registered user."""

    id: UUID
    email: str
    display_name: str
    password_hash: str
    created_at: datetime

    def __post_init__(self) -> None:
        """Validate entity invariants."""
        if not self.email or "@" not in self.email:
            raise ValueError("Invalid email format: email must contain '@'")
        if not self.display_name or not self.display_name.strip():
            raise ValueError("Display name cannot be empty")
