"""Unit tests for AgentService."""

from datetime import datetime
from uuid import uuid4

import pytest

from application.services.agent_service import AgentService
from domain.entities.memory import Memory
from domain.entities.message import Message
from domain.enums import MemoryImportance, MemoryType, MessageRole


def _make_message(role: MessageRole, content: str) -> Message:
    """Helper to build a Message entity."""
    return Message(
        id=uuid4(),
        conversation_id=uuid4(),
        role=role,
        content=content,
        metadata_json=None,
        created_at=datetime.utcnow(),
    )


def _make_memory(content: str, importance: MemoryImportance = MemoryImportance.MEDIUM) -> Memory:
    """Helper to build a Memory entity."""
    now = datetime.utcnow()
    return Memory(
        id=uuid4(),
        user_id=uuid4(),
        type=MemoryType.PREFERENCE,
        content=content,
        importance=importance,
        source_message_id=None,
        is_active=True,
        created_at=now,
        updated_at=now,
    )


# ---------------------------------------------------------------------------
# build_prompt tests
# ---------------------------------------------------------------------------


def test_build_prompt_system_message_is_first() -> None:
    """First message in result has role='system'."""
    service = AgentService()
    result = service.build_prompt([], [], "Hello")

    assert result[0].role == "system"


def test_build_prompt_includes_memory_context() -> None:
    """When memories are provided, system message content contains 'User Context'."""
    service = AgentService()
    memories = [_make_memory("User prefers dark mode")]
    result = service.build_prompt(memories, [], "Hello")

    assert "User Context" in result[0].content


def test_build_prompt_no_memory_context_when_empty() -> None:
    """When no memories are provided, system message doesn't contain 'User Context'."""
    service = AgentService()
    result = service.build_prompt([], [], "Hello")

    assert "User Context" not in result[0].content


def test_build_prompt_limits_history_to_10() -> None:
    """When 15 messages are provided, only the last 10 appear in the prompt."""
    service = AgentService()
    messages = [
        _make_message(MessageRole.USER, f"message {i}") for i in range(15)
    ]
    result = service.build_prompt([], messages, "current message")

    # result = [system] + [last 10 history messages] + [current user message]
    history_messages = result[1:-1]
    assert len(history_messages) == 10

    # Verify they are the last 10 (messages 5–14)
    expected_contents = [f"message {i}" for i in range(5, 15)]
    actual_contents = [m.content for m in history_messages]
    assert actual_contents == expected_contents


def test_build_prompt_current_message_is_last() -> None:
    """Last message in result has role='user' and the correct content."""
    service = AgentService()
    result = service.build_prompt([], [], "my current question")

    last = result[-1]
    assert last.role == "user"
    assert last.content == "my current question"


# ---------------------------------------------------------------------------
# _format_memories tests
# ---------------------------------------------------------------------------


def test_format_memories_limits_to_5() -> None:
    """When 7 memories are provided, only 5 appear in the formatted output."""
    service = AgentService()
    memories = [_make_memory(f"memory content {i}") for i in range(7)]
    formatted = service._format_memories(memories)

    lines = formatted.strip().splitlines()
    assert len(lines) == 5
