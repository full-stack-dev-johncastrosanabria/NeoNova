"""Unit tests for application use cases."""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from application.dtos.auth_dtos import LoginDTO, RegisterUserDTO
from application.dtos.feedback_dtos import CreateFeedbackDTO
from application.dtos.message_dtos import SendMessageDTO
from application.interfaces.llm_provider import LLMResponse
from application.services.agent_service import AgentService
from application.services.memory_service import MemoryService
from application.use_cases.auth_use_cases import LoginUseCase, RegisterUserUseCase
from application.use_cases.feedback_use_cases import CreateFeedbackUseCase
from application.use_cases.message_use_cases import SendMessageUseCase
from domain.entities.conversation import Conversation
from domain.entities.feedback import Feedback
from domain.entities.memory import Memory
from domain.entities.message import Message
from domain.entities.user import User
from domain.enums import MemoryImportance, MemoryType, MessageRole


# ---------------------------------------------------------------------------
# RegisterUserUseCase tests
# ---------------------------------------------------------------------------


async def test_register_user_duplicate_email_raises(
    mock_user_repo: AsyncMock,
    mock_auth_service: MagicMock,
    sample_user: User,
) -> None:
    """When user_repo.find_by_email returns an existing user, raises ValueError."""
    mock_user_repo.find_by_email.return_value = sample_user

    use_case = RegisterUserUseCase(mock_user_repo, mock_auth_service)
    dto = RegisterUserDTO(
        email="test@example.com",
        password="password123",
        display_name="Test User",
    )

    with pytest.raises(ValueError, match="Email already registered"):
        await use_case.execute(dto)


async def test_register_user_success(
    mock_user_repo: AsyncMock,
    mock_auth_service: MagicMock,
    sample_user: User,
) -> None:
    """When no existing user, creates and returns a new user."""
    mock_user_repo.find_by_email.return_value = None
    mock_auth_service.hash_password.return_value = "hashed_pw"
    mock_user_repo.create.return_value = sample_user

    use_case = RegisterUserUseCase(mock_user_repo, mock_auth_service)
    dto = RegisterUserDTO(
        email="new@example.com",
        password="password123",
        display_name="New User",
    )

    result = await use_case.execute(dto)

    assert result is sample_user
    mock_user_repo.create.assert_called_once()


# ---------------------------------------------------------------------------
# LoginUseCase tests
# ---------------------------------------------------------------------------


async def test_login_user_not_found_raises(
    mock_user_repo: AsyncMock,
    mock_auth_service: MagicMock,
) -> None:
    """When user_repo.find_by_email returns None, raises ValueError."""
    mock_user_repo.find_by_email.return_value = None

    use_case = LoginUseCase(mock_user_repo, mock_auth_service)
    dto = LoginDTO(email="nobody@example.com", password="password123")

    with pytest.raises(ValueError, match="Invalid credentials"):
        await use_case.execute(dto)


async def test_login_wrong_password_raises(
    mock_user_repo: AsyncMock,
    mock_auth_service: MagicMock,
    sample_user: User,
) -> None:
    """When verify_password returns False, raises ValueError."""
    mock_user_repo.find_by_email.return_value = sample_user
    mock_auth_service.verify_password.return_value = False

    use_case = LoginUseCase(mock_user_repo, mock_auth_service)
    dto = LoginDTO(email="test@example.com", password="wrongpassword")

    with pytest.raises(ValueError, match="Invalid credentials"):
        await use_case.execute(dto)


async def test_login_success(
    mock_user_repo: AsyncMock,
    mock_auth_service: MagicMock,
    sample_user: User,
) -> None:
    """Successful login returns a (token, user) tuple."""
    mock_user_repo.find_by_email.return_value = sample_user
    mock_auth_service.verify_password.return_value = True
    mock_auth_service.create_access_token.return_value = "jwt_token_abc"

    use_case = LoginUseCase(mock_user_repo, mock_auth_service)
    dto = LoginDTO(email="test@example.com", password="correctpassword")

    token, user = await use_case.execute(dto)

    assert token == "jwt_token_abc"
    assert user is sample_user


# ---------------------------------------------------------------------------
# SendMessageUseCase tests
# ---------------------------------------------------------------------------


async def test_send_message_wrong_conversation_owner_raises(
    mock_conversation_repo: AsyncMock,
    mock_message_repo: AsyncMock,
    mock_memory_repo: AsyncMock,
    mock_llm_provider: AsyncMock,
) -> None:
    """When conversation.user_id != user_id, raises ValueError."""
    other_user_id = uuid4()
    requesting_user_id = uuid4()

    now = datetime.utcnow()
    conversation = Conversation(
        id=uuid4(),
        user_id=other_user_id,  # owned by someone else
        title="Other's Conversation",
        created_at=now,
        updated_at=now,
    )
    mock_conversation_repo.find_by_id.return_value = conversation

    memory_service = MemoryService(mock_memory_repo)
    agent_service = AgentService()

    use_case = SendMessageUseCase(
        mock_conversation_repo,
        mock_message_repo,
        memory_service,
        agent_service,
        mock_llm_provider,
    )
    dto = SendMessageDTO(
        conversation_id=conversation.id,
        content="Hello",
    )

    with pytest.raises(ValueError, match="Conversation not found"):
        await use_case.execute(dto, requesting_user_id)


async def test_send_message_conversation_not_found_raises(
    mock_conversation_repo: AsyncMock,
    mock_message_repo: AsyncMock,
    mock_memory_repo: AsyncMock,
    mock_llm_provider: AsyncMock,
) -> None:
    """When conversation_repo.find_by_id returns None, raises ValueError."""
    mock_conversation_repo.find_by_id.return_value = None

    memory_service = MemoryService(mock_memory_repo)
    agent_service = AgentService()

    use_case = SendMessageUseCase(
        mock_conversation_repo,
        mock_message_repo,
        memory_service,
        agent_service,
        mock_llm_provider,
    )
    dto = SendMessageDTO(conversation_id=uuid4(), content="Hello")

    with pytest.raises(ValueError, match="Conversation not found"):
        await use_case.execute(dto, uuid4())


# ---------------------------------------------------------------------------
# CreateFeedbackUseCase tests
# ---------------------------------------------------------------------------


async def test_create_feedback_message_not_found_raises(
    mock_message_repo: AsyncMock,
    mock_feedback_repo: AsyncMock,
    mock_memory_repo: AsyncMock,
) -> None:
    """When message_repo.find_by_id returns None, raises ValueError."""
    mock_message_repo.find_by_id.return_value = None

    memory_service = MemoryService(mock_memory_repo)
    use_case = CreateFeedbackUseCase(
        mock_message_repo, mock_feedback_repo, memory_service
    )
    dto = CreateFeedbackDTO(
        message_id=uuid4(),
        rating=4,
        comment=None,
        correction=None,
    )

    with pytest.raises(ValueError, match="Message not found"):
        await use_case.execute(dto, uuid4())


async def test_create_feedback_duplicate_raises(
    mock_message_repo: AsyncMock,
    mock_feedback_repo: AsyncMock,
    mock_memory_repo: AsyncMock,
    sample_message: Message,
) -> None:
    """When feedback_repo.find_by_message returns existing feedback, raises ValueError."""
    mock_message_repo.find_by_id.return_value = sample_message

    existing_feedback = Feedback(
        id=uuid4(),
        message_id=sample_message.id,
        user_id=uuid4(),
        rating=5,
        comment=None,
        correction=None,
        created_at=datetime.utcnow(),
    )
    mock_feedback_repo.find_by_message.return_value = existing_feedback

    memory_service = MemoryService(mock_memory_repo)
    use_case = CreateFeedbackUseCase(
        mock_message_repo, mock_feedback_repo, memory_service
    )
    dto = CreateFeedbackDTO(
        message_id=sample_message.id,
        rating=3,
        comment=None,
        correction=None,
    )

    with pytest.raises(ValueError, match="Feedback already exists"):
        await use_case.execute(dto, uuid4())
