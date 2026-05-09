"""Unit tests for MemoryService."""

from datetime import datetime, timedelta
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from application.services.memory_service import MemoryService
from domain.entities.memory import Memory
from domain.enums import MemoryImportance, MemoryType


def _make_memory(
    user_id,
    importance: MemoryImportance,
    content: str = "some content",
    created_at: datetime | None = None,
) -> Memory:
    """Helper to build a Memory entity with the given importance."""
    now = created_at or datetime.utcnow()
    return Memory(
        id=uuid4(),
        user_id=user_id,
        type=MemoryType.FACT,
        content=content,
        importance=importance,
        source_message_id=None,
        is_active=True,
        created_at=now,
        updated_at=now,
    )


# ---------------------------------------------------------------------------
# get_active_memories — sorting tests
# ---------------------------------------------------------------------------


async def test_get_active_memories_sorted_by_importance(
    mock_memory_repo: AsyncMock,
) -> None:
    """Returned list is sorted by importance descending."""
    user_id = uuid4()
    low = _make_memory(user_id, MemoryImportance.LOW)
    high = _make_memory(user_id, MemoryImportance.HIGH)
    medium = _make_memory(user_id, MemoryImportance.MEDIUM)
    critical = _make_memory(user_id, MemoryImportance.CRITICAL)

    mock_memory_repo.find_active_by_user.return_value = [low, high, medium, critical]

    service = MemoryService(mock_memory_repo)
    result = await service.get_active_memories(user_id)

    importances = [m.importance.value for m in result]
    assert importances == sorted(importances, reverse=True)


async def test_get_active_memories_sorted_by_recency(
    mock_memory_repo: AsyncMock,
) -> None:
    """Memories with the same importance are sorted by created_at descending."""
    user_id = uuid4()
    base = datetime.utcnow()
    older = _make_memory(
        user_id, MemoryImportance.MEDIUM, created_at=base - timedelta(hours=2)
    )
    newer = _make_memory(
        user_id, MemoryImportance.MEDIUM, created_at=base - timedelta(hours=1)
    )
    newest = _make_memory(
        user_id, MemoryImportance.MEDIUM, created_at=base
    )

    mock_memory_repo.find_active_by_user.return_value = [older, newest, newer]

    service = MemoryService(mock_memory_repo)
    result = await service.get_active_memories(user_id)

    # All same importance — should be ordered newest first
    assert result[0].created_at >= result[1].created_at >= result[2].created_at


# ---------------------------------------------------------------------------
# extract_memory_from_correction tests
# ---------------------------------------------------------------------------


async def test_extract_memory_from_correction_creates_correction_type(
    mock_memory_repo: AsyncMock,
) -> None:
    """Created memory has type=MemoryType.CORRECTION."""
    user_id = uuid4()
    message_id = uuid4()

    # Return the memory that was passed to create()
    mock_memory_repo.create.side_effect = lambda m: m

    service = MemoryService(mock_memory_repo)
    memory = await service.extract_memory_from_correction(
        "Please use metric units", message_id, user_id
    )

    assert memory.type == MemoryType.CORRECTION


async def test_extract_memory_from_correction_creates_high_importance(
    mock_memory_repo: AsyncMock,
) -> None:
    """Created memory has importance=MemoryImportance.HIGH."""
    user_id = uuid4()
    message_id = uuid4()

    mock_memory_repo.create.side_effect = lambda m: m

    service = MemoryService(mock_memory_repo)
    memory = await service.extract_memory_from_correction(
        "Always respond in Spanish", message_id, user_id
    )

    assert memory.importance == MemoryImportance.HIGH


async def test_extract_memory_from_correction_links_source_message(
    mock_memory_repo: AsyncMock,
) -> None:
    """Created memory has source_message_id set to the provided message_id."""
    user_id = uuid4()
    message_id = uuid4()

    mock_memory_repo.create.side_effect = lambda m: m

    service = MemoryService(mock_memory_repo)
    memory = await service.extract_memory_from_correction(
        "Correction text", message_id, user_id
    )

    assert memory.source_message_id == message_id
