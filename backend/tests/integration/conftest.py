"""Integration test fixtures for NeoNova backend."""

import asyncio
import os
from typing import AsyncGenerator

import httpx
import pytest
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool

# Set test environment variables before importing app modules
# Use in-memory SQLite for integration tests (no external DB required)
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-testing-only")
os.environ.setdefault("ALGORITHM", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
os.environ.setdefault("OPENAI_API_KEY", "test-key")
os.environ.setdefault("OPENAI_MODEL", "gpt-4")
os.environ.setdefault("LLM_PROVIDER", "openai")
os.environ.setdefault("CORS_ALLOW_ORIGINS", "http://localhost:5173")

# Import after setting environment variables
from infrastructure.database import Base
from main import create_app


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for the test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def test_db_engine():
    """Create an in-memory SQLite database engine for testing."""
    # Use SQLite in-memory database for fast tests
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False,
    )

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Cleanup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
async def test_db_session(test_db_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session."""
    from sqlalchemy.ext.asyncio import async_sessionmaker

    async_session = async_sessionmaker(
        test_db_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session() as session:
        yield session


@pytest.fixture
async def test_client(test_db_engine) -> AsyncGenerator[httpx.AsyncClient, None]:
    """Create a test HTTP client with a test database."""
    from sqlalchemy.ext.asyncio import async_sessionmaker
    from unittest.mock import AsyncMock
    from api.dependencies import get_send_message_use_case

    # Create async session factory for the test database
    async_session = async_sessionmaker(
        test_db_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    # Override the get_db dependency
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        async with async_session() as session:
            yield session

    # Create the app
    app = create_app()

    # Import and override the dependency
    from infrastructure.database import get_db
    app.dependency_overrides[get_db] = override_get_db

    # Mock the LLM provider for send_message_use_case
    def mock_send_message_use_case(
        db: AsyncSession = Depends(override_get_db),
    ):
        """Provide a mocked SendMessageUseCase with a mock LLM provider."""
        from application.use_cases.message_use_cases import SendMessageUseCase
        from application.services.memory_service import MemoryService
        from application.services.agent_service import AgentService
        from infrastructure.repositories.conversation_repository import (
            ConversationRepository,
        )
        from infrastructure.repositories.message_repository import (
            MessageRepository,
        )
        from infrastructure.repositories.memory_repository import (
            MemoryRepository,
        )
        from unittest.mock import AsyncMock

        # Create a mock LLM provider
        mock_llm = AsyncMock()
        mock_response = AsyncMock()
        mock_response.content = "This is a mock assistant response."
        mock_response.model = "gpt-4"
        mock_response.usage = {"prompt_tokens": 10, "completion_tokens": 20}
        mock_response.finish_reason = "stop"
        mock_llm.generate_completion = AsyncMock(return_value=mock_response)

        memory_repo = MemoryRepository(db)
        memory_service = MemoryService(memory_repo=memory_repo)
        return SendMessageUseCase(
            conversation_repo=ConversationRepository(db),
            message_repo=MessageRepository(db),
            memory_service=memory_service,
            agent_service=AgentService(),
            llm_provider=mock_llm,
        )

    app.dependency_overrides[get_send_message_use_case] = (
        mock_send_message_use_case
    )

    # Create async client with ASGITransport
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    # Cleanup
    app.dependency_overrides.clear()


@pytest.fixture
async def test_user(test_db_session: AsyncSession):
    """Create a test user in the database."""
    from application.services.auth_service import AuthService
    from domain.entities.user import User
    from infrastructure.repositories.user_repository import UserRepository
    from uuid import uuid4
    from datetime import datetime

    auth_service = AuthService()
    user_repo = UserRepository(test_db_session)

    user = User(
        id=uuid4(),
        email="testuser@example.com",
        display_name="Test User",
        password_hash=auth_service.hash_password("password123"),
        created_at=datetime.utcnow(),
    )

    created_user = await user_repo.create(user)
    return created_user


@pytest.fixture
async def test_user_token(test_user):
    """Generate a valid JWT token for the test user."""
    from application.services.auth_service import AuthService

    auth_service = AuthService()
    token = auth_service.create_access_token(test_user.id)
    return token


@pytest.fixture
async def test_conversation(test_client, test_user_token):
    """Create a test conversation via the API."""
    response = await test_client.post(
        "/conversations/",
        json={"title": "Test Conversation"},
        headers={"Authorization": f"Bearer {test_user_token}"},
    )
    assert response.status_code == 201
    conv_data = response.json()
    
    # Return a simple object with the conversation data
    from uuid import UUID
    from dataclasses import dataclass
    
    @dataclass
    class ConversationData:
        id: UUID
        user_id: UUID
        title: str
        created_at: str
        updated_at: str
    
    return ConversationData(
        id=UUID(conv_data["id"]),
        user_id=UUID(conv_data["user_id"]),
        title=conv_data["title"],
        created_at=conv_data["created_at"],
        updated_at=conv_data["updated_at"],
    )
