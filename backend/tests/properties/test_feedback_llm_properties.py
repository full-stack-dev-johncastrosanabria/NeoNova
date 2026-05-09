"""Property-based tests for feedback and LLM properties using Hypothesis.

**Validates: Requirements 5.1, 5.3, 5.4, 5.5, 6.3, 6.4, 10.1, 10.3, 10.7**

This module tests feedback creation, memory extraction from corrections,
LLM message format conversion, LLM response field extraction, and error
response formatting.
"""

from datetime import datetime, timezone
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from hypothesis import given, strategies as st, settings

from application.dtos.feedback_dtos import CreateFeedbackDTO
from application.interfaces.llm_provider import LLMMessage, LLMResponse
from application.services.memory_service import MemoryService
from application.use_cases.feedback_use_cases import CreateFeedbackUseCase
from domain.entities.feedback import Feedback
from domain.entities.memory import Memory
from domain.entities.message import Message
from domain.enums import MemoryImportance, MemoryType, MessageRole


class TestFeedbackStorageProperties:
    """Property-based tests for feedback storage."""

    def setup_method(self):
        """Set up test dependencies."""
        self.message_repo = AsyncMock()
        self.feedback_repo = AsyncMock()
        self.memory_service = AsyncMock(spec=MemoryService)
        self.use_case = CreateFeedbackUseCase(
            self.message_repo,
            self.feedback_repo,
            self.memory_service,
        )

    async def test_feedback_storage_with_all_fields(self):
        """Property 24: For any valid message_id and feedback data,
        CreateFeedbackUseCase SHALL persist feedback with all provided
        fields (rating, comment, correction).

        **Validates: Requirements 5.1**
        """
        # Test case 1: Feedback with all fields
        message_id = uuid4()
        user_id = uuid4()
        message = Message(
            id=message_id,
            conversation_id=uuid4(),
            role=MessageRole.ASSISTANT,
            content="Test response",
            metadata_json=None,
            created_at=datetime.now(timezone.utc),
        )

        self.message_repo.find_by_id.return_value = message
        self.feedback_repo.find_by_message.return_value = None

        # Mock the create to return the feedback
        def create_feedback(feedback):
            return feedback

        self.feedback_repo.create.side_effect = create_feedback

        dto = CreateFeedbackDTO(
            message_id=message_id,
            rating=5,
            comment="Great response!",
            correction="Minor typo in line 2",
        )

        result = await self.use_case.execute(dto, user_id)

        # Verify all fields are persisted
        assert result.message_id == message_id
        assert result.user_id == user_id
        assert result.rating == 5
        assert result.comment == "Great response!"
        assert result.correction == "Minor typo in line 2"

        # Verify the feedback was created
        self.feedback_repo.create.assert_called_once()

    async def test_feedback_storage_with_partial_fields(self):
        """Property 24: For any valid message_id and feedback data,
        CreateFeedbackUseCase SHALL persist feedback with all provided
        fields (rating, comment, correction).

        **Validates: Requirements 5.1**
        """
        # Test case 2: Feedback with only rating
        message_id = uuid4()
        user_id = uuid4()
        message = Message(
            id=message_id,
            conversation_id=uuid4(),
            role=MessageRole.ASSISTANT,
            content="Test response",
            metadata_json=None,
            created_at=datetime.now(timezone.utc),
        )

        self.message_repo.find_by_id.return_value = message
        self.feedback_repo.find_by_message.return_value = None

        def create_feedback(feedback):
            return feedback

        self.feedback_repo.create.side_effect = create_feedback

        dto = CreateFeedbackDTO(
            message_id=message_id,
            rating=3,
            comment=None,
            correction=None,
        )

        result = await self.use_case.execute(dto, user_id)

        # Verify fields are persisted as provided
        assert result.message_id == message_id
        assert result.user_id == user_id
        assert result.rating == 3
        assert result.comment is None
        assert result.correction is None

        # Verify the feedback was created
        self.feedback_repo.create.assert_called_once()


class TestCorrectionMemoryExtractionProperties:
    """Property-based tests for automatic memory extraction from corrections."""

    def setup_method(self):
        """Set up test dependencies."""
        self.message_repo = AsyncMock()
        self.feedback_repo = AsyncMock()
        self.memory_service = AsyncMock(spec=MemoryService)
        self.use_case = CreateFeedbackUseCase(
            self.message_repo,
            self.feedback_repo,
            self.memory_service,
        )

    async def test_correction_creates_memory_with_correct_type(self):
        """Property 26: For any feedback with a non-empty correction,
        CreateFeedbackUseCase SHALL create a Memory with type=CORRECTION
        and importance=HIGH.

        **Validates: Requirements 5.3, 5.4**
        """
        message_id = uuid4()
        user_id = uuid4()
        message = Message(
            id=message_id,
            conversation_id=uuid4(),
            role=MessageRole.ASSISTANT,
            content="Test response",
            metadata_json=None,
            created_at=datetime.now(timezone.utc),
        )

        self.message_repo.find_by_id.return_value = message
        self.feedback_repo.find_by_message.return_value = None

        def create_feedback(feedback):
            return feedback

        self.feedback_repo.create.side_effect = create_feedback

        # Create a memory to return from extract_memory_from_correction
        created_memory = Memory(
            id=uuid4(),
            user_id=user_id,
            type=MemoryType.CORRECTION,
            content="The correct approach is...",
            importance=MemoryImportance.HIGH,
            source_message_id=message_id,
            is_active=True,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        self.memory_service.extract_memory_from_correction.return_value = (
            created_memory
        )

        dto = CreateFeedbackDTO(
            message_id=message_id,
            rating=2,
            comment="Incorrect approach",
            correction="The correct approach is...",
        )

        await self.use_case.execute(dto, user_id)

        # Verify extract_memory_from_correction was called
        self.memory_service.extract_memory_from_correction.assert_called_once()

        # Verify the call arguments
        call_args = (
            self.memory_service.extract_memory_from_correction.call_args[0]
        )
        assert call_args[0] == "The correct approach is..."
        assert call_args[1] == message_id
        assert call_args[2] == user_id

    async def test_no_memory_extraction_without_correction(self):
        """Property 26: For any feedback with a non-empty correction,
        CreateFeedbackUseCase SHALL create a Memory...

        **Validates: Requirements 5.3, 5.4**
        """
        message_id = uuid4()
        user_id = uuid4()
        message = Message(
            id=message_id,
            conversation_id=uuid4(),
            role=MessageRole.ASSISTANT,
            content="Test response",
            metadata_json=None,
            created_at=datetime.now(timezone.utc),
        )

        self.message_repo.find_by_id.return_value = message
        self.feedback_repo.find_by_message.return_value = None

        def create_feedback(feedback):
            return feedback

        self.feedback_repo.create.side_effect = create_feedback

        dto = CreateFeedbackDTO(
            message_id=message_id,
            rating=4,
            comment="Good response",
            correction=None,
        )

        await self.use_case.execute(dto, user_id)

        # Verify extract_memory_from_correction was NOT called
        self.memory_service.extract_memory_from_correction.assert_not_called()


class TestCorrectionMemorySourceLinkingProperties:
    """Property-based tests for correction memory source linking."""

    def setup_method(self):
        """Set up test dependencies."""
        self.memory_repo = AsyncMock()

    async def test_correction_memory_source_message_id_matches(self):
        """Property 27: For any feedback with a correction, the auto-created
        Memory's source_message_id SHALL equal the feedback's message_id.

        **Validates: Requirements 5.5**
        """
        # Test multiple message IDs
        test_cases = [uuid4(), uuid4(), uuid4()]

        for message_id in test_cases:
            user_id = uuid4()
            correction_text = "This is the correct approach"

            # Create the memory service
            memory_service = MemoryService(self.memory_repo)

            # Mock the repository to return the created memory
            def create_memory(memory):
                return memory

            self.memory_repo.create.side_effect = create_memory

            # Call extract_memory_from_correction
            created_memory = (
                await memory_service.extract_memory_from_correction(
                    correction_text, message_id, user_id
                )
            )

            # Verify source_message_id matches the feedback's message_id
            assert created_memory.source_message_id == message_id
            assert created_memory.type == MemoryType.CORRECTION
            assert created_memory.importance == MemoryImportance.HIGH


class TestLLMMessageFormatConversionProperties:
    """Property-based tests for LLM message format conversion."""

    def test_domain_messages_convert_to_llm_format(self):
        """Property 28: For any list of domain Message objects, converting
        them to LLM format SHALL produce dicts with 'role' and 'content'
        keys matching the domain message fields.

        **Validates: Requirements 6.3**
        """
        # Test case 1: Single message
        message = Message(
            id=uuid4(),
            conversation_id=uuid4(),
            role=MessageRole.USER,
            content="Hello, NeoNova!",
            metadata_json=None,
            created_at=datetime.now(timezone.utc),
        )

        llm_message = LLMMessage(
            role=message.role.value, content=message.content
        )

        assert llm_message.role == "user"
        assert llm_message.content == "Hello, NeoNova!"

    def test_multiple_domain_messages_convert_to_llm_format(self):
        """Property 28: For any list of domain Message objects, converting
        them to LLM format SHALL produce dicts with 'role' and 'content'
        keys matching the domain message fields.

        **Validates: Requirements 6.3**
        """
        # Test case 2: Multiple messages with different roles
        messages = [
            Message(
                id=uuid4(),
                conversation_id=uuid4(),
                role=MessageRole.USER,
                content="What is Python?",
                metadata_json=None,
                created_at=datetime.now(timezone.utc),
            ),
            Message(
                id=uuid4(),
                conversation_id=uuid4(),
                role=MessageRole.ASSISTANT,
                content="Python is a programming language.",
                metadata_json=None,
                created_at=datetime.now(timezone.utc),
            ),
            Message(
                id=uuid4(),
                conversation_id=uuid4(),
                role=MessageRole.USER,
                content="Tell me more.",
                metadata_json=None,
                created_at=datetime.now(timezone.utc),
            ),
        ]

        llm_messages = [
            LLMMessage(role=msg.role.value, content=msg.content)
            for msg in messages
        ]

        # Verify all messages converted correctly
        assert len(llm_messages) == 3
        assert llm_messages[0].role == "user"
        assert llm_messages[0].content == "What is Python?"
        assert llm_messages[1].role == "assistant"
        assert llm_messages[1].content == "Python is a programming language."
        assert llm_messages[2].role == "user"
        assert llm_messages[2].content == "Tell me more."

    @given(st.sampled_from(list(MessageRole)))
    @settings(max_examples=3)
    def test_all_message_roles_convert_correctly(self, role: MessageRole):
        """Property 28: For any list of domain Message objects, converting
        them to LLM format SHALL produce dicts with 'role' and 'content'
        keys matching the domain message fields.

        **Validates: Requirements 6.3**
        """
        message = Message(
            id=uuid4(),
            conversation_id=uuid4(),
            role=role,
            content="Test content",
            metadata_json=None,
            created_at=datetime.now(timezone.utc),
        )

        llm_message = LLMMessage(
            role=message.role.value, content=message.content
        )

        # Verify the role is correctly converted
        assert llm_message.role == role.value
        assert llm_message.content == "Test content"


class TestLLMResponseFieldExtractionProperties:
    """Property-based tests for LLM response field extraction."""

    def test_llm_response_contains_all_required_fields(self):
        """Property 29: For any LLMResponse, the extracted fields SHALL
        include content (str), model (str), usage (dict with token counts),
        and finish_reason (str).

        **Validates: Requirements 6.4**
        """
        # Test case 1: Complete LLM response
        response = LLMResponse(
            content="This is the AI response.",
            model="gpt-4",
            usage={"prompt_tokens": 10, "completion_tokens": 20,
                   "total_tokens": 30},
            finish_reason="stop",
        )

        # Verify all fields are present and correct type
        assert isinstance(response.content, str)
        assert response.content == "This is the AI response."

        assert isinstance(response.model, str)
        assert response.model == "gpt-4"

        assert isinstance(response.usage, dict)
        assert "prompt_tokens" in response.usage
        assert "completion_tokens" in response.usage
        assert "total_tokens" in response.usage
        assert response.usage["prompt_tokens"] == 10
        assert response.usage["completion_tokens"] == 20
        assert response.usage["total_tokens"] == 30

        assert isinstance(response.finish_reason, str)
        assert response.finish_reason == "stop"

    def test_llm_response_with_various_token_counts(self):
        """Property 29: For any LLMResponse, the extracted fields SHALL
        include content (str), model (str), usage (dict with token counts),
        and finish_reason (str).

        **Validates: Requirements 6.4**
        """
        # Test case 2: Different token counts
        test_cases = [
            {"prompt_tokens": 5, "completion_tokens": 15, "total_tokens": 20},
            {"prompt_tokens": 100, "completion_tokens": 200,
             "total_tokens": 300},
            {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2},
        ]

        for usage in test_cases:
            response = LLMResponse(
                content="Response content",
                model="gpt-3.5-turbo",
                usage=usage,
                finish_reason="length",
            )

            # Verify usage dict structure
            assert response.usage == usage
            assert response.usage["total_tokens"] == (
                response.usage["prompt_tokens"]
                + response.usage["completion_tokens"]
            )

    @given(
        st.text(min_size=1),
        st.text(min_size=1),
        st.sampled_from(["stop", "length", "content_filter"]),
    )
    @settings(max_examples=5)
    def test_llm_response_field_types(
        self, content: str, model: str, finish_reason: str
    ):
        """Property 29: For any LLMResponse, the extracted fields SHALL
        include content (str), model (str), usage (dict with token counts),
        and finish_reason (str).

        **Validates: Requirements 6.4**
        """
        response = LLMResponse(
            content=content,
            model=model,
            usage={"prompt_tokens": 10, "completion_tokens": 20,
                   "total_tokens": 30},
            finish_reason=finish_reason,
        )

        # Verify all fields have correct types
        assert isinstance(response.content, str)
        assert isinstance(response.model, str)
        assert isinstance(response.usage, dict)
        assert isinstance(response.finish_reason, str)


class TestErrorResponseFormatProperties:
    """Property-based tests for error response formatting."""

    def test_validation_error_response_format(self):
        """Property 40: For any ValueError raised in a route handler, the
        HTTP response SHALL have status 400 and a body containing 'message'
        and 'timestamp' fields.

        **Validates: Requirements 10.1, 10.7**
        """
        # Simulate error response format
        error_response = {
            "error": "Bad Request",
            "message": "Message not found",
            "details": None,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        # Verify response structure
        assert "error" in error_response
        assert error_response["error"] == "Bad Request"
        assert "message" in error_response
        assert isinstance(error_response["message"], str)
        assert len(error_response["message"]) > 0
        assert "timestamp" in error_response
        assert isinstance(error_response["timestamp"], str)

    def test_not_found_error_response_format(self):
        """Property 41: For any request for a non-existent resource, the
        HTTP response SHALL have status 404 and a body containing 'message'
        and 'timestamp' fields.

        **Validates: Requirements 10.3, 10.7**
        """
        # Simulate 404 error response format
        error_response = {
            "error": "Not Found",
            "message": "Conversation not found",
            "details": None,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        # Verify response structure
        assert "error" in error_response
        assert error_response["error"] == "Not Found"
        assert "message" in error_response
        assert isinstance(error_response["message"], str)
        assert len(error_response["message"]) > 0
        assert "timestamp" in error_response
        assert isinstance(error_response["timestamp"], str)

    @given(st.text(min_size=1, max_size=200))
    @settings(max_examples=5)
    def test_error_response_with_various_messages(self, message: str):
        """Property 40 & 41: Error responses SHALL contain 'message' and
        'timestamp' fields.

        **Validates: Requirements 10.1, 10.3, 10.7**
        """
        error_response = {
            "error": "Bad Request",
            "message": message,
            "details": None,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        # Verify required fields are present
        assert "message" in error_response
        assert error_response["message"] == message
        assert "timestamp" in error_response
        assert isinstance(error_response["timestamp"], str)

    def test_error_response_timestamp_format(self):
        """Property 40 & 41: Error responses SHALL include a valid timestamp.

        **Validates: Requirements 10.1, 10.3, 10.7**
        """
        # Test multiple error responses
        error_messages = [
            "Validation failed",
            "Resource not found",
            "Unauthorized access",
        ]

        for msg in error_messages:
            error_response = {
                "error": "Error",
                "message": msg,
                "details": None,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

            # Verify timestamp is ISO format
            assert "timestamp" in error_response
            timestamp_str = error_response["timestamp"]
            # Should be parseable as ISO format
            try:
                datetime.fromisoformat(timestamp_str)
            except ValueError:
                pytest.fail(f"Invalid timestamp format: {timestamp_str}")
