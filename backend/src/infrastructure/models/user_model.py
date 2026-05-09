"""SQLAlchemy ORM model for users."""

import uuid

from sqlalchemy import DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from infrastructure.database import Base


class UserModel(Base):
    """SQLAlchemy model for the users table."""

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )
    display_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    created_at: Mapped[object] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
    )

    # Relationships
    conversations: Mapped[list] = relationship(
        "ConversationModel",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    memories: Mapped[list] = relationship(
        "MemoryModel",
        back_populates="user",
        cascade="all, delete-orphan",
    )
