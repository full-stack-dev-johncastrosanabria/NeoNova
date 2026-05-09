"""Unit tests for domain entities."""

from datetime import datetime
from uuid import uuid4

import pytest

from domain.entities.conversation import Conversation
from domain.entities.feedback import Feedback
from domain.entities.memory import Memory
from domain.entities.message import Message
from domain.entities.user import User
from domain.enums import MemoryImportance, MemoryType, MessageRole


# ---------------------------------------------------------------------------
# User entity tests
# ---------------------------------------------------------------------------


def test_user_valid_creation() -> None:
    """Creates User with valid data without raising an exception."""
    user = User(
        id=uuid4(),
        email="alice@example.com",
        display_name="Alice",
        password_hash="hashed",
        created_at=datetime.utcnow(),
    )
    assert user.email == "alice@example.com"
    assert user.display_name == "Alice"


def test_user_invalid_email() -> None:
    """Email without '@' raises ValueError."""
    with pytest.raises(ValueError, match="email must contain"):
        User(
            id=uuid4(),
            email="invalidemail",
            display_name="Alice",
            password_hash="hashed",
            created_at=datetime.utcnow(),
        )


def test_user_empty_display_name() -> None:
    """Empty display_name raises ValueError."""
    with pytest.raises(ValueError, match="Display name cannot be empty"):
        User(
            id=uuid4(),
            email="alice@example.com",
            display_name="",
            password_hash="hashed",
            created_at=datetime.utcnow(),
        )


# ---------------------------------------------------------------------------
# Message entity tests
# ---------------------------------------------------------------------------


def test_message_empty_content() -> None:
    """Empty content raises ValueError."""
    with pytest.raises(ValueError, match="content cannot be empty"):
        Message(
            id=uuid4(),
            conversation_id=uuid4(),
            role=MessageRole.USER,
            content="",
            metadata_json=None,
            created_at=datetime.utcnow(),
        )


def test_message_invalid_role() -> None:
    """Non-MessageRole role raises ValueError."""
    with pytest.raises(ValueError, match="Invalid message role"):
        Message(
            id=uuid4(),
            conversation_id=uuid4(),
            role="user",  # type: ignore[arg-type]
            content="Hello",
            metadata_json=None,
            created_at=datetime.utcnow(),
        )


# ---------------------------------------------------------------------------
# Feedback entity tests
# ---------------------------------------------------------------------------


def test_feedback_rating_too_low() -> None:
    """Rating of 0 raises ValueError."""
    with pytest.raises(ValueError, match="Rating must be between 1 and 5"):
        Feedback(
            id=uuid4(),
            message_id=uuid4(),
            user_id=uuid4(),
            rating=0,
            comment=None,
            correction=None,
            created_at=datetime.utcnow(),
        )


def test_feedback_rating_too_high() -> None:
    """Rating of 6 raises ValueError."""
    with pytest.raises(ValueError, match="Rating must be between 1 and 5"):
        Feedback(
            id=uuid4(),
            message_id=uuid4(),
            user_id=uuid4(),
            rating=6,
            comment=None,
            correction=None,
            created_at=datetime.utcnow(),
        )


def test_feedback_valid_rating() -> None:
    """Rating of 3 creates Feedback without error."""
    feedback = Feedback(
        id=uuid4(),
        message_id=uuid4(),
        user_id=uuid4(),
        rating=3,
        comment=None,
        correction=None,
        created_at=datetime.utcnow(),
    )
    assert feedback.rating == 3


# ---------------------------------------------------------------------------
# Memory entity tests
# ---------------------------------------------------------------------------


def test_memory_empty_content() -> None:
    """Empty content raises ValueError."""
    now = datetime.utcnow()
    with pytest.raises(ValueError, match="Memory content cannot be empty"):
        Memory(
            id=uuid4(),
            user_id=uuid4(),
            type=MemoryType.FACT,
            content="",
            importance=MemoryImportance.LOW,
            source_message_id=None,
            is_active=True,
            created_at=now,
            updated_at=now,
        )


def test_memory_deactivate() -> None:
    """deactivate() sets is_active=False and updates updated_at."""
    now = datetime.utcnow()
    memory = Memory(
        id=uuid4(),
        user_id=uuid4(),
        type=MemoryType.FACT,
        content="Some fact",
        importance=MemoryImportance.LOW,
        source_message_id=None,
        is_active=True,
        created_at=now,
        updated_at=now,
    )
    original_updated_at = memory.updated_at
    memory.deactivate()

    assert memory.is_active is False
    assert memory.updated_at >= original_updated_at


# ---------------------------------------------------------------------------
# Conversation entity tests
# ---------------------------------------------------------------------------


def test_conversation_update_title() -> None:
    """update_title() changes title and updates updated_at."""
    now = datetime.utcnow()
    conversation = Conversation(
        id=uuid4(),
        user_id=uuid4(),
        title="Old Title",
        created_at=now,
        updated_at=now,
    )
    original_updated_at = conversation.updated_at
    conversation.update_title("New Title")

    assert conversation.title == "New Title"
    assert conversation.updated_at >= original_updated_at


def test_conversation_update_title_empty() -> None:
    """Empty title raises ValueError."""
    now = datetime.utcnow()
    conversation = Conversation(
        id=uuid4(),
        user_id=uuid4(),
        title="Some Title",
        created_at=now,
        updated_at=now,
    )
    with pytest.raises(ValueError, match="Title cannot be empty"):
        conversation.update_title("")
