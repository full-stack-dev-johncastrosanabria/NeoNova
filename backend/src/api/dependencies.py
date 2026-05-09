"""FastAPI dependency factory functions for all application use cases."""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.config import get_settings
from application.services.agent_service import AgentService
from application.services.auth_service import AuthService
from application.services.memory_service import MemoryService
from application.use_cases.auth_use_cases import (
    LoginUseCase,
    RegisterUserUseCase,
)
from application.use_cases.conversation_use_cases import (
    CreateConversationUseCase,
    DeleteConversationUseCase,
    ListConversationsUseCase,
)
from application.use_cases.feedback_use_cases import CreateFeedbackUseCase
from application.use_cases.memory_use_cases import (
    CreateMemoryUseCase,
    DeactivateMemoryUseCase,
    ListMemoriesUseCase,
)
from application.use_cases.message_use_cases import (
    ListMessagesUseCase,
    SendMessageUseCase,
)
from infrastructure.database import get_db
from infrastructure.llm_providers.factory import create_llm_provider
from infrastructure.repositories.conversation_repository import (
    ConversationRepository,
)
from infrastructure.repositories.feedback_repository import FeedbackRepository
from infrastructure.repositories.memory_repository import MemoryRepository
from infrastructure.repositories.message_repository import MessageRepository
from infrastructure.repositories.user_repository import UserRepository


def get_register_use_case(
    db: AsyncSession = Depends(get_db),
) -> RegisterUserUseCase:
    """Provide a configured :class:`RegisterUserUseCase` instance."""
    return RegisterUserUseCase(
        user_repo=UserRepository(db),
        auth_service=AuthService(),
    )


def get_login_use_case(
    db: AsyncSession = Depends(get_db),
) -> LoginUseCase:
    """Provide a configured :class:`LoginUseCase` instance."""
    return LoginUseCase(
        user_repo=UserRepository(db),
        auth_service=AuthService(),
    )


def get_create_conversation_use_case(
    db: AsyncSession = Depends(get_db),
) -> CreateConversationUseCase:
    """Provide a configured :class:`CreateConversationUseCase` instance."""
    return CreateConversationUseCase(
        conversation_repo=ConversationRepository(db),
    )


def get_list_conversations_use_case(
    db: AsyncSession = Depends(get_db),
) -> ListConversationsUseCase:
    """Provide a configured :class:`ListConversationsUseCase` instance."""
    return ListConversationsUseCase(
        conversation_repo=ConversationRepository(db),
    )


def get_delete_conversation_use_case(
    db: AsyncSession = Depends(get_db),
) -> DeleteConversationUseCase:
    """Provide a configured :class:`DeleteConversationUseCase` instance."""
    return DeleteConversationUseCase(
        conversation_repo=ConversationRepository(db),
    )


def get_send_message_use_case(
    db: AsyncSession = Depends(get_db),
) -> SendMessageUseCase:
    """Provide a configured :class:`SendMessageUseCase` instance.

    Wires up all required repositories, MemoryService, AgentService, and
    the LLM provider resolved from application settings.
    """
    settings = get_settings()
    memory_repo = MemoryRepository(db)
    memory_service = MemoryService(memory_repo=memory_repo)
    return SendMessageUseCase(
        conversation_repo=ConversationRepository(db),
        message_repo=MessageRepository(db),
        memory_service=memory_service,
        agent_service=AgentService(),
        llm_provider=create_llm_provider(settings),
    )


def get_list_messages_use_case(
    db: AsyncSession = Depends(get_db),
) -> ListMessagesUseCase:
    """Provide a configured :class:`ListMessagesUseCase` instance."""
    return ListMessagesUseCase(
        conversation_repo=ConversationRepository(db),
        message_repo=MessageRepository(db),
    )


def get_create_memory_use_case(
    db: AsyncSession = Depends(get_db),
) -> CreateMemoryUseCase:
    """Provide a configured :class:`CreateMemoryUseCase` instance."""
    return CreateMemoryUseCase(
        memory_repo=MemoryRepository(db),
    )


def get_list_memories_use_case(
    db: AsyncSession = Depends(get_db),
) -> ListMemoriesUseCase:
    """Provide a configured :class:`ListMemoriesUseCase` instance."""
    memory_repo = MemoryRepository(db)
    return ListMemoriesUseCase(
        memory_service=MemoryService(memory_repo=memory_repo),
    )


def get_deactivate_memory_use_case(
    db: AsyncSession = Depends(get_db),
) -> DeactivateMemoryUseCase:
    """Provide a configured :class:`DeactivateMemoryUseCase` instance."""
    return DeactivateMemoryUseCase(
        memory_repo=MemoryRepository(db),
    )


def get_create_feedback_use_case(
    db: AsyncSession = Depends(get_db),
) -> CreateFeedbackUseCase:
    """Provide a configured :class:`CreateFeedbackUseCase` instance."""
    memory_repo = MemoryRepository(db)
    return CreateFeedbackUseCase(
        message_repo=MessageRepository(db),
        feedback_repo=FeedbackRepository(db),
        memory_service=MemoryService(memory_repo=memory_repo),
    )
