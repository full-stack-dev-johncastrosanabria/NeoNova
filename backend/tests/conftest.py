"""Shared pytest fixtures for NeoNova backend tests."""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from application.interfaces.llm_provider import ILLMProvider
from application.interfaces.repositories import (
    IConversationRepository,
    IFeedbackRepository,
    IMemoryRepository,
    IMessageRepository,
    IUserRepository,
)
from application.services.auth_service import AuthService
from domain.entities.conversation import Conversation
from domain.entities.memory import Memory
from domain.entities.message import Message
from domain.entities.user import User
from domain.enums import MemoryImportance, MemoryType, MessageRole


# ---------------------------------------------------------------------------
# Mock repository fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_user_repo() -> AsyncMock:
    """AsyncMock implementing IUserRepository."""
    mock = AsyncMock(spec=IUserRepository)
    return mock


@pytest.fixture
def mock_conversation_repo() -> AsyncMock:
    """AsyncMock implementing IConversationRepository."""
    mock = AsyncMock(spec=IConversationRepository)
    return mock


@pytest.fixture
def mock_message_repo() -> AsyncMock:
    """AsyncMock implementing IMessageRepository."""
    mock = AsyncMock(spec=IMessageRepository)
    return mock


@pytest.fixture
def mock_memory_repo() -> AsyncMock:
    """AsyncMock implementing IMemoryRepository."""
    mock = AsyncMock(spec=IMemoryRepository)
    return mock


@pytest.fixture
def mock_feedback_repo() -> AsyncMock:
    """AsyncMock implementing IFeedbackRepository."""
    mock = AsyncMock(spec=IFeedbackRepository)
    return mock


@pytest.fixture
def mock_llm_provider() -> AsyncMock:
    """AsyncMock implementing ILLMProvider."""
    mock = AsyncMock(spec=ILLMProvider)
    return mock


@pytest.fixture
def mock_auth_service() -> MagicMock:
    """MagicMock for AuthService."""
    mock = MagicMock(spec=AuthService)
    return mock


# ---------------------------------------------------------------------------
# Sample entity fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def sample_user() -> User:
    """A valid User entity for use in tests."""
    return User(
        id=uuid4(),
        email="test@example.com",
        display_name="Test User",
        password_hash="hashed_password",
        created_at=datetime.utcnow(),
    )


@pytest.fixture
def sample_conversation(sample_user: User) -> Conversation:
    """A valid Conversation entity for use in tests."""
    now = datetime.utcnow()
    return Conversation(
        id=uuid4(),
        user_id=sample_user.id,
        title="Test Conversation",
        created_at=now,
        updated_at=now,
    )


@pytest.fixture
def sample_message(sample_conversation: Conversation) -> Message:
    """A valid Message entity for use in tests."""
    return Message(
        id=uuid4(),
        conversation_id=sample_conversation.id,
        role=MessageRole.USER,
        content="Hello, NeoNova!",
        metadata_json=None,
        created_at=datetime.utcnow(),
    )


@pytest.fixture
def sample_memory(sample_user: User) -> Memory:
    """A valid Memory entity for use in tests."""
    now = datetime.utcnow()
    return Memory(
        id=uuid4(),
        user_id=sample_user.id,
        type=MemoryType.PREFERENCE,
        content="User prefers concise answers",
        importance=MemoryImportance.MEDIUM,
        source_message_id=None,
        is_active=True,
        created_at=now,
        updated_at=now,
    )
