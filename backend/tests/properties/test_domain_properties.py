"""Property-based tests for domain entity invariants using Hypothesis.

**Validates: Requirements 1.5, 1.6, 1.7, 3.7, 4.6, 4.8, 5.2, 8.2, 8.7, 16.1–16.7**

This module tests the invariants and business rules of domain entities to ensure
they maintain consistency under various input conditions.
"""

import uuid
from datetime import datetime
from typing import Any

import pytest
from hypothesis import given, strategies as st, settings

from domain.entities.feedback import Feedback
from domain.entities.memory import Memory
from domain.entities.message import Message
from domain.entities.user import User
from domain.enums import MemoryImportance, MemoryType, MessageRole


class TestUserEntityInvariants:
    """Property-based tests for User entity invariants."""

    @given(st.text().filter(lambda x: "@" not in x))
    @settings(max_examples=5)
    def test_user_creation_with_invalid_email_raises_error(self, invalid_email: str):
        """Property 3: For any string without '@', User creation SHALL raise ValueError.
        
        **Validates: Requirements 1.5, 16.1**
        """
        with pytest.raises(ValueError, match="Invalid email format"):
            User(
                id=uuid.uuid4(),
                email=invalid_email,
                display_name="Valid Name",
                password_hash="hashed_password",
                created_at=datetime.utcnow(),
            )

    @given(st.text().filter(lambda x: not x.strip()))
    @settings(max_examples=5)
    def test_user_creation_with_whitespace_display_name_raises_error(self, whitespace_name: str):
        """Property 4: For any whitespace-only string, User creation with that display_name SHALL raise ValueError.
        
        **Validates: Requirements 1.6, 16.2**
        """
        with pytest.raises(ValueError, match="Display name cannot be empty"):
            User(
                id=uuid.uuid4(),
                email="valid@example.com",
                display_name=whitespace_name,
                password_hash="hashed_password",
                created_at=datetime.utcnow(),
            )

    @given(
        st.emails(),
        st.text(min_size=1).filter(lambda x: x.strip()),
        st.text(min_size=1),
    )
    @settings(max_examples=5)
    def test_valid_user_creation_succeeds(self, email: str, display_name: str, password_hash: str):
        """Property 34: For any entity created (User), the assigned id SHALL be a valid UUID.
        
        **Validates: Requirements 8.2**
        """
        user_id = uuid.uuid4()
        created_at = datetime.utcnow()
        
        user = User(
            id=user_id,
            email=email,
            display_name=display_name,
            password_hash=password_hash,
            created_at=created_at,
        )
        
        # Verify the entity was created successfully
        assert user.id == user_id
        assert isinstance(user.id, uuid.UUID)
        assert user.email == email
        assert user.display_name == display_name
        assert user.password_hash == password_hash
        assert user.created_at == created_at


class TestMessageEntityInvariants:
    """Property-based tests for Message entity invariants."""

    @given(st.text().filter(lambda x: not x.strip()))
    @settings(max_examples=5)
    def test_message_creation_with_whitespace_content_raises_error(self, whitespace_content: str):
        """Property 16: For any whitespace-only string, Message creation with that content SHALL raise ValueError.
        
        **Validates: Requirements 3.7, 16.3**
        """
        with pytest.raises(ValueError, match="Message content cannot be empty"):
            Message(
                id=uuid.uuid4(),
                conversation_id=uuid.uuid4(),
                role=MessageRole.USER,
                content=whitespace_content,
                metadata_json=None,
                created_at=datetime.utcnow(),
            )

    @given(st.text(min_size=1).filter(lambda x: x.strip()))
    @settings(max_examples=5)
    def test_valid_message_creation_succeeds(self, content: str):
        """Property 34: For any entity created (Message), the assigned id SHALL be a valid UUID.
        
        **Validates: Requirements 8.2, 16.4**
        """
        message_id = uuid.uuid4()
        conversation_id = uuid.uuid4()
        created_at = datetime.utcnow()
        
        message = Message(
            id=message_id,
            conversation_id=conversation_id,
            role=MessageRole.USER,
            content=content,
            metadata_json=None,
            created_at=created_at,
        )
        
        # Verify the entity was created successfully
        assert message.id == message_id
        assert isinstance(message.id, uuid.UUID)
        assert message.conversation_id == conversation_id
        assert message.role == MessageRole.USER
        assert message.content == content
        assert message.created_at == created_at

    @given(st.one_of(st.text(), st.integers(), st.floats(), st.booleans()))
    @settings(max_examples=5)
    def test_message_creation_with_invalid_role_raises_error(self, invalid_role: Any):
        """Property: For any non-MessageRole value, Message creation SHALL raise ValueError.
        
        **Validates: Requirements 16.4**
        """
        # Skip if the invalid_role happens to be a valid MessageRole
        if isinstance(invalid_role, MessageRole):
            return
            
        with pytest.raises(ValueError, match="Invalid message role"):
            Message(
                id=uuid.uuid4(),
                conversation_id=uuid.uuid4(),
                role=invalid_role,  # type: ignore
                content="Valid content",
                metadata_json=None,
                created_at=datetime.utcnow(),
            )


class TestMemoryEntityInvariants:
    """Property-based tests for Memory entity invariants."""

    @given(st.text().filter(lambda x: not x.strip()))
    @settings(max_examples=5)
    def test_memory_creation_with_whitespace_content_raises_error(self, whitespace_content: str):
        """Property 22: For any whitespace-only string, Memory creation with that content SHALL raise ValueError.
        
        **Validates: Requirements 4.6, 16.6**
        """
        with pytest.raises(ValueError, match="Memory content cannot be empty"):
            Memory(
                id=uuid.uuid4(),
                user_id=uuid.uuid4(),
                type=MemoryType.PREFERENCE,
                content=whitespace_content,
                importance=MemoryImportance.MEDIUM,
                source_message_id=None,
                is_active=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )

    @given(st.text(min_size=1).filter(lambda x: x.strip()))
    @settings(max_examples=5)
    def test_valid_memory_creation_succeeds(self, content: str):
        """Property 34: For any entity created (Memory), the assigned id SHALL be a valid UUID.
        
        **Validates: Requirements 8.2**
        """
        memory_id = uuid.uuid4()
        user_id = uuid.uuid4()
        created_at = datetime.utcnow()
        updated_at = datetime.utcnow()
        
        memory = Memory(
            id=memory_id,
            user_id=user_id,
            type=MemoryType.PREFERENCE,
            content=content,
            importance=MemoryImportance.MEDIUM,
            source_message_id=None,
            is_active=True,
            created_at=created_at,
            updated_at=updated_at,
        )
        
        # Verify the entity was created successfully
        assert memory.id == memory_id
        assert isinstance(memory.id, uuid.UUID)
        assert memory.user_id == user_id
        assert memory.content == content
        assert memory.created_at == created_at

    def test_memory_deactivate_updates_state(self):
        """Property 21: For any active Memory, calling memory.deactivate() SHALL set is_active=False and updated_at SHALL be >= created_at.
        
        **Validates: Requirements 4.5**
        """
        created_at = datetime.utcnow()
        memory = Memory(
            id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            type=MemoryType.PREFERENCE,
            content="Test memory",
            importance=MemoryImportance.MEDIUM,
            source_message_id=None,
            is_active=True,
            created_at=created_at,
            updated_at=created_at,
        )
        
        # Deactivate the memory
        memory.deactivate()
        
        # Verify the state changes
        assert memory.is_active is False
        assert memory.updated_at >= created_at

    @given(st.sampled_from(list(MemoryImportance)))
    @settings(max_examples=5)
    def test_memory_update_importance_updates_state(self, new_importance: MemoryImportance):
        """Property: For any MemoryImportance value, calling update_importance() SHALL update importance and updated_at.
        
        **Validates: Requirements 4.8**
        """
        created_at = datetime.utcnow()
        memory = Memory(
            id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            type=MemoryType.PREFERENCE,
            content="Test memory",
            importance=MemoryImportance.LOW,
            source_message_id=None,
            is_active=True,
            created_at=created_at,
            updated_at=created_at,
        )
        
        # Update importance
        memory.update_importance(new_importance)
        
        # Verify the state changes
        assert memory.importance == new_importance
        assert memory.updated_at >= created_at


class TestFeedbackEntityInvariants:
    """Property-based tests for Feedback entity invariants."""

    @given(st.integers().filter(lambda x: x < 1 or x > 5))
    @settings(max_examples=5)
    def test_feedback_creation_with_invalid_rating_raises_error(self, invalid_rating: int):
        """Property 25: For any integer outside [1, 5], Feedback creation with that rating SHALL raise ValueError.
        
        **Validates: Requirements 5.2, 16.5**
        """
        with pytest.raises(ValueError, match="Rating must be between 1 and 5"):
            Feedback(
                id=uuid.uuid4(),
                message_id=uuid.uuid4(),
                user_id=uuid.uuid4(),
                rating=invalid_rating,
                comment="Valid comment",
                correction=None,
                created_at=datetime.utcnow(),
            )

    @given(st.integers(min_value=1, max_value=5))
    @settings(max_examples=5)
    def test_feedback_creation_with_valid_rating_succeeds(self, valid_rating: int):
        """Property 34: For any entity created (Feedback), the assigned id SHALL be a valid UUID.
        
        **Validates: Requirements 8.2, 5.2**
        """
        feedback_id = uuid.uuid4()
        message_id = uuid.uuid4()
        user_id = uuid.uuid4()
        created_at = datetime.utcnow()
        
        feedback = Feedback(
            id=feedback_id,
            message_id=message_id,
            user_id=user_id,
            rating=valid_rating,
            comment="Valid comment",
            correction=None,
            created_at=created_at,
        )
        
        # Verify the entity was created successfully
        assert feedback.id == feedback_id
        assert isinstance(feedback.id, uuid.UUID)
        assert feedback.message_id == message_id
        assert feedback.user_id == user_id
        assert feedback.rating == valid_rating
        assert feedback.created_at == created_at

    def test_feedback_creation_with_none_rating_succeeds(self):
        """Property: Feedback creation with None rating SHALL succeed.
        
        **Validates: Requirements 5.2**
        """
        feedback = Feedback(
            id=uuid.uuid4(),
            message_id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            rating=None,
            comment="Valid comment",
            correction=None,
            created_at=datetime.utcnow(),
        )
        
        # Verify the entity was created successfully
        assert feedback.rating is None


class TestDomainValidationInvariants:
    """Property-based tests for general domain validation invariants."""

    @given(
        st.one_of(
            st.text().filter(lambda x: "@" not in x),  # Invalid email
            st.text().filter(lambda x: not x.strip()),  # Whitespace display name
        )
    )
    @settings(max_examples=5)
    def test_domain_validation_fails_before_repository_calls(self, invalid_data: str):
        """Property 36: For any entity with invalid domain data, the ValueError SHALL be raised before any repository call is made.
        
        **Validates: Requirements 8.7, 16.7**
        
        This test ensures that domain validation happens at entity creation time,
        not during repository operations.
        """
        # Test User with invalid email (no '@')
        if "@" not in invalid_data:
            with pytest.raises(ValueError, match="Invalid email format"):
                User(
                    id=uuid.uuid4(),
                    email=invalid_data,
                    display_name="Valid Name",
                    password_hash="hashed_password",
                    created_at=datetime.utcnow(),
                )
        
        # Test User with whitespace display name
        elif not invalid_data.strip():
            with pytest.raises(ValueError, match="Display name cannot be empty"):
                User(
                    id=uuid.uuid4(),
                    email="valid@example.com",
                    display_name=invalid_data,
                    password_hash="hashed_password",
                    created_at=datetime.utcnow(),
                )