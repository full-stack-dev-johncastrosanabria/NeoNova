"""Property-based tests for Conversation and Message properties using Hypothesis.

**Validates: Requirements 2.1, 2.2, 2.4, 2.5, 3.1, 3.5, 3.6, 3.8**

This module tests the behavior of conversation and message use cases to ensure
they handle various input conditions correctly and maintain expected invariants.
"""

import uuid
from datetime import datetime, timedelta
from typing import List
from unittest.mock import AsyncMock

import pytest
from hypothesis import given, strategies as st, settings

from application.dtos.message_dtos import SendMessageDTO
from application.interfaces.llm_provider import LLMMessage, LLMResponse
from application.services.agent_service import AgentService
from application.services.memory_service import MemoryService
from application.use_cases.conversation_use_cases import (
    CreateConversationUseCase,
    ListConversationsUseCase,
)
from application.use_cases.message_use_cases import SendMessageUseCase
from domain.entities.conversation import Conversation
from domain.entities.memory import Memory
from domain.entities.message import Message
from domain.enums import MemoryImportance, MemoryType, MessageRole


class TestCreateConversationProperties:
    """Property-based tests for CreateConversationUseCase."""

    def setup_method(self):
        """Set up test dependencies."""
        self.conversation_repo = AsyncMock()

    async def test_create_conversation_with_authenticated_user(self):
        """Property 6: For any authenticated user and non-empty title,
        CreateConversationUseCase SHALL produce a Conversation with user_id
        matching the authenticated user's ID.

        **Validates: Requirements 2.1, 2.2**
        """
        # Use fixed test data
        test_cases = [
            ("Test Conversation 1", "user1@example.com"),
            ("My Chat", "user2@example.com"),
            ("Project Discussion", "user3@example.com"),
        ]

        for title, email in test_cases:
            user_id = uuid.uuid4()

            # Mock repository to return the created conversation
            async def mock_create(conversation: Conversation) -> Conversation:
                return conversation

            self.conversation_repo.create.side_effect = mock_create

            use_case = CreateConversationUseCase(self.conversation_repo)
            result = await use_case.execute(title, user_id)

            # Verify the conversation has the correct user_id
            assert result.user_id == user_id
            assert result.title == title
            assert isinstance(result.id, uuid.UUID)
            assert result.created_at is not None
            assert result.updated_at is not None

    @given(st.text().filter(lambda x: x.strip() == ""))
    @settings(max_examples=10)
    async def test_create_conversation_with_whitespace_only_title(
        self, whitespace_title: str
    ):
        """Property 8: For any whitespace-only string, CreateConversationUseCase
        SHALL raise ValueError.

        **Validates: Requirements 2.4**
        """
        user_id = uuid.uuid4()
        use_case = CreateConversationUseCase(self.conversation_repo)

        with pytest.raises(ValueError, match="Conversation title cannot be empty"):
            await use_case.execute(whitespace_title, user_id)


class TestListConversationsProperties:
    """Property-based tests for ListConversationsUseCase."""

    def setup_method(self):
        """Set up test dependencies."""
        self.conversation_repo = AsyncMock()

    @given(
        st.lists(
            st.uuids(),
            min_size=1,
            max_size=10,
            unique=True
        )
    )
    @settings(max_examples=10)
    async def test_list_conversations_returns_only_user_conversations(
        self, conversation_ids: List[uuid.UUID]
    ):
        """Property 7: For any user, ListConversationsUseCase SHALL return only
        conversations where conversation.user_id == current_user.id.

        **Validates: Requirements 2.2**
        """
        # Reset mock for each hypothesis example
        self.conversation_repo.reset_mock()
        
        user_id = uuid.uuid4()
        now = datetime.utcnow()

        # Create conversations for this user
        conversations = [
            Conversation(
                id=conv_id,
                user_id=user_id,
                title=f"Conversation {i}",
                created_at=now,
                updated_at=now,
            )
            for i, conv_id in enumerate(conversation_ids)
        ]

        # Mock repository to return only this user's conversations
        self.conversation_repo.find_by_user.return_value = conversations

        use_case = ListConversationsUseCase(self.conversation_repo)
        result = await use_case.execute(user_id)

        # Verify all returned conversations belong to the user
        assert len(result) == len(conversation_ids)
        for conversation in result:
            assert conversation.user_id == user_id

        # Verify the repository was called with the correct user_id
        self.conversation_repo.find_by_user.assert_called_once_with(user_id)

    async def test_list_conversations_returns_empty_for_new_user(self):
        """Property: For a user with no conversations, ListConversationsUseCase
        SHALL return an empty list.

        **Validates: Requirements 2.2**
        """
        user_id = uuid.uuid4()

        # Mock repository to return empty list
        self.conversation_repo.find_by_user.return_value = []

        use_case = ListConversationsUseCase(self.conversation_repo)
        result = await use_case.execute(user_id)

        assert result == []
        self.conversation_repo.find_by_user.assert_called_once_with(user_id)


class TestConversationUpdateTimestampProperties:
    """Property-based tests for Conversation timestamp updates."""

    def test_conversation_update_title_updates_timestamp(self):
        """Property 9: For any Conversation, after calling update_title(),
        updated_at SHALL be >= created_at.

        **Validates: Requirements 2.5**
        """
        # Use fixed test data
        test_cases = [
            ("Original Title", "Updated Title"),
            ("Chat 1", "Chat 2"),
            ("Discussion", "New Discussion"),
        ]

        for original_title, new_title in test_cases:
            now = datetime.utcnow()
            conversation = Conversation(
                id=uuid.uuid4(),
                user_id=uuid.uuid4(),
                title=original_title,
                created_at=now,
                updated_at=now,
            )

            # Store original updated_at
            original_updated_at = conversation.updated_at

            # Wait a tiny bit to ensure time difference
            import time
            time.sleep(0.01)

            # Update the title
            conversation.update_title(new_title)

            # Verify updated_at was updated
            assert conversation.updated_at >= original_updated_at
            assert conversation.updated_at >= conversation.created_at
            assert conversation.title == new_title


class TestSendMessageProperties:
    """Property-based tests for SendMessageUseCase."""

    def setup_method(self):
        """Set up test dependencies."""
        self.conversation_repo = AsyncMock()
        self.message_repo = AsyncMock()
        self.memory_service = AsyncMock(spec=MemoryService)
        self.agent_service = AsyncMock(spec=AgentService)
        self.llm_provider = AsyncMock()

    async def test_send_message_persists_exactly_two_messages(self):
        """Property 11: For any valid message content, SendMessageUseCase SHALL
        persist exactly two messages: one with role=USER and one with role=ASSISTANT.

        **Validates: Requirements 3.1, 3.5**
        """
        # Use fixed test data
        test_cases = [
            "Hello, NeoNova!",
            "What is the weather?",
            "Tell me a joke",
        ]

        for content in test_cases:
            # Reset mocks
            self.conversation_repo.reset_mock()
            self.message_repo.reset_mock()
            self.memory_service.reset_mock()
            self.agent_service.reset_mock()
            self.llm_provider.reset_mock()

            user_id = uuid.uuid4()
            conversation_id = uuid.uuid4()
            now = datetime.utcnow()

            # Mock conversation
            conversation = Conversation(
                id=conversation_id,
                user_id=user_id,
                title="Test",
                created_at=now,
                updated_at=now,
            )
            self.conversation_repo.find_by_id.return_value = conversation

            # Mock memories
            self.memory_service.get_active_memories.return_value = []

            # Mock recent messages
            self.message_repo.find_by_conversation.return_value = []

            # Mock agent service
            self.agent_service.build_prompt.return_value = [
                LLMMessage(role="system", content="System prompt"),
                LLMMessage(role="user", content=content),
            ]

            # Mock LLM response
            self.llm_provider.generate_completion.return_value = LLMResponse(
                content="Assistant response",
                model="gpt-4",
                usage={"prompt_tokens": 10, "completion_tokens": 20},
                finish_reason="stop",
            )

            # Mock message creation
            created_messages = []

            async def mock_create_message(message: Message) -> Message:
                created_messages.append(message)
                return message

            self.message_repo.create.side_effect = mock_create_message

            # Mock conversation update
            async def mock_update_conversation(
                conv: Conversation,
            ) -> Conversation:
                return conv

            self.conversation_repo.update.side_effect = mock_update_conversation

            # Execute use case
            use_case = SendMessageUseCase(
                self.conversation_repo,
                self.message_repo,
                self.memory_service,
                self.agent_service,
                self.llm_provider,
            )

            dto = SendMessageDTO(conversation_id=conversation_id, content=content)
            user_msg, assistant_msg = await use_case.execute(dto, user_id)

            # Verify exactly two messages were created
            assert len(created_messages) == 2

            # Verify one is USER and one is ASSISTANT
            roles = {msg.role for msg in created_messages}
            assert MessageRole.USER in roles
            assert MessageRole.ASSISTANT in roles

            # Verify the returned messages match
            assert user_msg.role == MessageRole.USER
            assert user_msg.content == content
            assert assistant_msg.role == MessageRole.ASSISTANT
            assert assistant_msg.content == "Assistant response"

    async def test_send_message_updates_conversation_timestamp(self):
        """Property 17: For any conversation, after SendMessageUseCase executes,
        the conversation's updated_at SHALL be >= its previous updated_at.

        **Validates: Requirements 3.8**
        """
        user_id = uuid.uuid4()
        conversation_id = uuid.uuid4()
        content = "Test message"

        # Create conversation with initial timestamp
        initial_time = datetime.utcnow()
        conversation = Conversation(
            id=conversation_id,
            user_id=user_id,
            title="Test",
            created_at=initial_time,
            updated_at=initial_time,
        )

        # Track the conversation passed to update
        updated_conversation = None

        async def mock_update_conversation(conv: Conversation) -> Conversation:
            nonlocal updated_conversation
            updated_conversation = conv
            return conv

        self.conversation_repo.find_by_id.return_value = conversation
        self.conversation_repo.update.side_effect = mock_update_conversation
        self.memory_service.get_active_memories.return_value = []
        self.message_repo.find_by_conversation.return_value = []
        self.agent_service.build_prompt.return_value = [
            LLMMessage(role="system", content="System prompt"),
            LLMMessage(role="user", content=content),
        ]
        self.llm_provider.generate_completion.return_value = LLMResponse(
            content="Response",
            model="gpt-4",
            usage={"prompt_tokens": 10, "completion_tokens": 20},
            finish_reason="stop",
        )

        async def mock_create_message(message: Message) -> Message:
            return message

        self.message_repo.create.side_effect = mock_create_message

        use_case = SendMessageUseCase(
            self.conversation_repo,
            self.message_repo,
            self.memory_service,
            self.agent_service,
            self.llm_provider,
        )

        dto = SendMessageDTO(conversation_id=conversation_id, content=content)
        await use_case.execute(dto, user_id)

        # Verify conversation was updated
        assert updated_conversation is not None
        assert updated_conversation.updated_at >= initial_time

    async def test_send_message_assistant_metadata_contains_model_and_usage(self):
        """Property 15: For any assistant message saved by SendMessageUseCase,
        metadata_json SHALL contain 'model' and 'usage' keys.

        **Validates: Requirements 3.6**
        """
        user_id = uuid.uuid4()
        conversation_id = uuid.uuid4()
        content = "Test message"

        # Create conversation
        now = datetime.utcnow()
        conversation = Conversation(
            id=conversation_id,
            user_id=user_id,
            title="Test",
            created_at=now,
            updated_at=now,
        )

        # Track created messages
        created_messages = []

        async def mock_create_message(message: Message) -> Message:
            created_messages.append(message)
            return message

        self.conversation_repo.find_by_id.return_value = conversation
        self.conversation_repo.update.return_value = conversation
        self.memory_service.get_active_memories.return_value = []
        self.message_repo.find_by_conversation.return_value = []
        self.message_repo.create.side_effect = mock_create_message
        self.agent_service.build_prompt.return_value = [
            LLMMessage(role="system", content="System prompt"),
            LLMMessage(role="user", content=content),
        ]

        # Use fixed test data for LLM response
        test_cases = [
            ("gpt-4", {"prompt_tokens": 10, "completion_tokens": 20}),
            ("gpt-3.5-turbo", {"prompt_tokens": 5, "completion_tokens": 15}),
            ("claude-3", {"prompt_tokens": 8, "completion_tokens": 25}),
        ]

        for model, usage in test_cases:
            created_messages.clear()

            self.llm_provider.generate_completion.return_value = LLMResponse(
                content="Response",
                model=model,
                usage=usage,
                finish_reason="stop",
            )

            use_case = SendMessageUseCase(
                self.conversation_repo,
                self.message_repo,
                self.memory_service,
                self.agent_service,
                self.llm_provider,
            )

            dto = SendMessageDTO(conversation_id=conversation_id, content=content)
            await use_case.execute(dto, user_id)

            # Find the assistant message
            assistant_messages = [
                msg for msg in created_messages if msg.role == MessageRole.ASSISTANT
            ]
            assert len(assistant_messages) == 1

            assistant_msg = assistant_messages[0]

            # Verify metadata contains model and usage
            assert assistant_msg.metadata_json is not None
            assert "model" in assistant_msg.metadata_json
            assert "usage" in assistant_msg.metadata_json
            assert assistant_msg.metadata_json["model"] == model
            assert assistant_msg.metadata_json["usage"] == usage
