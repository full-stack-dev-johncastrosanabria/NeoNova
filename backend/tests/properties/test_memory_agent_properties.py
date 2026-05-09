"""Property-based tests for Memory and Agent Service properties using Hypothesis.

**Validates: Requirements 3.2, 3.3, 3.4, 4.3, 4.4, 4.5, 7.1, 7.3, 7.5, 7.6, 7.7**

This module tests the behavior of MemoryService and AgentService to ensure
they handle various input conditions correctly and maintain expected invariants.
"""

import uuid
from datetime import datetime, timedelta
from typing import List
from unittest.mock import AsyncMock

import pytest
from hypothesis import given, strategies as st, settings

from application.interfaces.llm_provider import LLMMessage
from application.services.agent_service import AgentService
from application.services.memory_service import MemoryService
from domain.entities.memory import Memory
from domain.entities.message import Message
from domain.enums import MemoryImportance, MemoryType, MessageRole


class TestMemoryServiceProperties:
    """Property-based tests for MemoryService behavior."""

    @given(
        st.lists(
            st.tuples(
                st.sampled_from(list(MemoryImportance)),
                st.datetimes(
                    min_value=datetime(2020, 1, 1),
                    max_value=datetime(2030, 12, 31)
                )
            ),
            min_size=2,
            max_size=10
        )
    )
    @settings(max_examples=10)
    async def test_get_active_memories_sorts_by_importance_then_created_at(
        self, importance_datetime_pairs: List[tuple[MemoryImportance, datetime]]
    ):
        """Property 19: For any list of active Memory objects with varying importance and created_at, 
        MemoryService.get_active_memories() SHALL return them sorted by importance desc, then created_at desc for ties.
        
        **Validates: Requirements 4.3, 4.4**
        """
        # Create memories with the given importance and datetime pairs
        memories = []
        user_id = uuid.uuid4()
        
        for i, (importance, created_at) in enumerate(importance_datetime_pairs):
            memory = Memory(
                id=uuid.uuid4(),
                user_id=user_id,
                type=MemoryType.PREFERENCE,
                content=f"Memory content {i}",
                importance=importance,
                source_message_id=None,
                is_active=True,
                created_at=created_at,
                updated_at=created_at,
            )
            memories.append(memory)
        
        # Mock repository
        mock_repo = AsyncMock()
        mock_repo.find_active_by_user.return_value = memories
        
        # Create service and call method
        service = MemoryService(mock_repo)
        result = await service.get_active_memories(user_id)
        
        # Verify sorting: importance desc, then created_at desc for ties
        for i in range(len(result) - 1):
            current = result[i]
            next_memory = result[i + 1]
            
            # Higher importance should come first
            if current.importance.value != next_memory.importance.value:
                assert current.importance.value > next_memory.importance.value
            else:
                # For same importance, more recent (later) created_at should come first
                assert current.created_at >= next_memory.created_at

    @given(
        st.lists(
            st.booleans(),
            min_size=5,
            max_size=15
        )
    )
    @settings(max_examples=10)
    async def test_get_active_memories_returns_only_active(self, is_active_flags: List[bool]):
        """Property 12: For any mix of active and inactive memories, get_active_memories() 
        SHALL return only memories where is_active=True.
        
        **Validates: Requirements 4.3**
        """
        # Create memories with mixed active/inactive status
        memories = []
        user_id = uuid.uuid4()
        now = datetime.utcnow()
        
        for i, is_active in enumerate(is_active_flags):
            memory = Memory(
                id=uuid.uuid4(),
                user_id=user_id,
                type=MemoryType.PREFERENCE,
                content=f"Memory content {i}",
                importance=MemoryImportance.MEDIUM,
                source_message_id=None,
                is_active=is_active,
                created_at=now,
                updated_at=now,
            )
            memories.append(memory)
        
        # Filter to only active memories (simulating repository behavior)
        active_memories = [m for m in memories if m.is_active]
        
        # Mock repository to return only active memories
        mock_repo = AsyncMock()
        mock_repo.find_active_by_user.return_value = active_memories
        
        # Create service and call method
        service = MemoryService(mock_repo)
        result = await service.get_active_memories(user_id)
        
        # Verify all returned memories are active
        assert all(memory.is_active for memory in result)
        
        # Verify we got the expected count
        expected_active_count = sum(is_active_flags)
        assert len(result) == expected_active_count

    def test_memory_deactivate_sets_inactive_and_updates_timestamp(self):
        """Property 21: For any active Memory, calling memory.deactivate() 
        SHALL set is_active=False and updated_at SHALL be >= created_at.
        
        **Validates: Requirements 4.5, 7.7**
        """
        created_at = datetime.utcnow()
        memory = Memory(
            id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            type=MemoryType.PREFERENCE,
            content="Test memory content",
            importance=MemoryImportance.HIGH,
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


class TestAgentServiceProperties:
    """Property-based tests for AgentService behavior."""

    @given(
        st.integers(min_value=6, max_value=20)
    )
    @settings(max_examples=10)
    def test_format_memories_limits_to_five(self, num_memories: int):
        """Property 20: For any list of N active memories where N > 5, 
        AgentService._format_memories() SHALL include at most 5 memories in the formatted output.
        
        **Validates: Requirements 7.5, 7.6**
        """
        # Create more than 5 memories
        memories = []
        now = datetime.utcnow()
        
        for i in range(num_memories):
            memory = Memory(
                id=uuid.uuid4(),
                user_id=uuid.uuid4(),
                type=MemoryType.PREFERENCE,
                content=f"Memory content {i}",
                importance=MemoryImportance.MEDIUM,
                source_message_id=None,
                is_active=True,
                created_at=now,
                updated_at=now,
            )
            memories.append(memory)
        
        # Create service and format memories
        service = AgentService()
        formatted = service._format_memories(memories)
        
        # Count the number of lines (each memory becomes one line)
        lines = formatted.split('\n') if formatted else []
        
        # Should have at most 5 lines
        assert len(lines) <= 5
        
        # If we had memories, should have exactly 5 lines (since num_memories > 5)
        if num_memories > 0:
            assert len(lines) == min(5, num_memories)

    @given(
        st.integers(min_value=11, max_value=25)
    )
    @settings(max_examples=10)
    def test_build_prompt_limits_message_history_to_ten(self, num_messages: int):
        """Property 13: For any conversation with N messages where N > 10, 
        AgentService.build_prompt() SHALL include at most 10 messages in the prompt 
        (excluding system message and current user message).
        
        **Validates: Requirements 3.3, 7.3**
        """
        # Create more than 10 messages
        messages = []
        conversation_id = uuid.uuid4()
        base_time = datetime.utcnow()
        
        for i in range(num_messages):
            role = MessageRole.USER if i % 2 == 0 else MessageRole.ASSISTANT
            message = Message(
                id=uuid.uuid4(),
                conversation_id=conversation_id,
                role=role,
                content=f"Message content {i}",
                metadata_json=None,
                created_at=base_time + timedelta(minutes=i),
            )
            messages.append(message)
        
        # Create service and build prompt
        service = AgentService()
        memories: List[Memory] = []  # Empty memories for this test
        user_content = "Current user message"
        
        result = service.build_prompt(memories, messages, user_content)
        
        # Count non-system, non-current-user messages
        # Result should have: 1 system + up to 10 history + 1 current user
        history_messages = [msg for msg in result if msg.role not in ["system", "user"] or 
                          (msg.role == "user" and msg.content != user_content)]
        
        # Should have at most 10 history messages
        assert len(history_messages) <= 10
        
        # Total should be: 1 system + history (≤10) + 1 current user
        assert len(result) <= 12  # 1 + 10 + 1
        
        # First message should be system
        assert result[0].role == "system"
        
        # Last message should be current user message
        assert result[-1].role == "user"
        assert result[-1].content == user_content

    def test_build_prompt_first_message_is_system_with_prompt(self):
        """Property 14: For any call to build_prompt(), the first message in the returned list 
        SHALL have role="system" and SHALL contain the SYSTEM_PROMPT constant.
        
        **Validates: Requirements 7.1**
        """
        service = AgentService()
        memories: List[Memory] = []
        messages: List[Message] = []
        user_content = "Test user message"
        
        result = service.build_prompt(memories, messages, user_content)
        
        # First message should be system
        assert len(result) > 0
        assert result[0].role == "system"
        
        # Should contain the system prompt
        assert AgentService.SYSTEM_PROMPT in result[0].content

    @given(
        st.integers(min_value=1, max_value=15)
    )
    @settings(max_examples=10)
    def test_build_prompt_message_order(self, num_messages: int):
        """Property 33: For any call to build_prompt() with history and a user message, 
        the messages SHALL be ordered: system, history (chronological), current user message last.
        
        **Validates: Requirements 7.7**
        """
        # Create messages with timestamps
        messages = []
        conversation_id = uuid.uuid4()
        base_time = datetime.utcnow()
        
        for i in range(num_messages):
            role = MessageRole.USER if i % 2 == 0 else MessageRole.ASSISTANT
            message = Message(
                id=uuid.uuid4(),
                conversation_id=conversation_id,
                role=role,
                content=f"History message {i}",
                metadata_json=None,
                created_at=base_time + timedelta(minutes=i),
            )
            messages.append(message)
        
        service = AgentService()
        memories: List[Memory] = []
        user_content = "Current user message"
        
        result = service.build_prompt(memories, messages, user_content)
        
        # Verify order: system first
        assert result[0].role == "system"
        
        # Last message should be current user message
        assert result[-1].role == "user"
        assert result[-1].content == user_content
        
        # Middle messages should be history in chronological order
        history_messages = result[1:-1]  # Exclude system and current user
        
        # Verify history messages are in chronological order
        # (They should match the order from messages[-10:])
        expected_history = messages[-10:] if len(messages) > 10 else messages
        
        assert len(history_messages) == len(expected_history)
        
        for i, (actual, expected) in enumerate(zip(history_messages, expected_history)):
            assert actual.role == expected.role.value
            assert actual.content == expected.content

    @given(
        st.lists(
            st.tuples(
                st.sampled_from(list(MemoryType)),
                st.text(min_size=1, max_size=100).filter(lambda x: x.strip())
            ),
            min_size=1,
            max_size=10
        )
    )
    @settings(max_examples=10)
    def test_format_memories_contains_type_and_content(
        self, memory_type_content_pairs: List[tuple[MemoryType, str]]
    ):
        """Property 32: For any Memory passed to _format_memories(), the formatted string 
        SHALL contain both memory.type.value and memory.content.
        
        **Validates: Requirements 7.5**
        """
        # Create memories from the generated pairs
        memories = []
        now = datetime.utcnow()
        
        for memory_type, content in memory_type_content_pairs:
            memory = Memory(
                id=uuid.uuid4(),
                user_id=uuid.uuid4(),
                type=memory_type,
                content=content,
                importance=MemoryImportance.MEDIUM,
                source_message_id=None,
                is_active=True,
                created_at=now,
                updated_at=now,
            )
            memories.append(memory)
        
        service = AgentService()
        formatted = service._format_memories(memories)
        
        # Check that each memory's type and content appear in the formatted string
        # (limited to first 5 memories)
        for memory in memories[:5]:
            assert memory.type.value in formatted
            assert memory.content in formatted
            
            # Should be formatted as "- [type] content"
            expected_line = f"- [{memory.type.value}] {memory.content}"
            assert expected_line in formatted