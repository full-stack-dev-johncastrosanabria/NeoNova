"""SQLAlchemy ORM model for messages."""

import uuid

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from infrastructure.database import Base


class MessageModel(Base):
    """SQLAlchemy model for the messages table."""

    __tablename__ = "messages"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    conversation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("conversations.id"),
        nullable=False,
        index=True,
    )
    # Stored as plain string: "user", "assistant", "system"
    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    metadata_json: Mapped[object] = mapped_column(
        JSONB,
        nullable=True,
    )
    created_at: Mapped[object] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
        index=True,
    )

    # Relationships
    conversation: Mapped[object] = relationship(
        "ConversationModel",
        back_populates="messages",
    )
    feedback: Mapped[object] = relationship(
        "FeedbackModel",
        back_populates="message",
        uselist=False,
    )
