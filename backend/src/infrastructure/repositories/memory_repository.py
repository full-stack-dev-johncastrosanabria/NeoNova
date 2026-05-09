"""SQLAlchemy implementation of IMemoryRepository."""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from application.interfaces.repositories import IMemoryRepository
from domain.entities.memory import Memory
from domain.enums import MemoryImportance, MemoryType
from infrastructure.models.memory_model import MemoryModel


class MemoryRepository(IMemoryRepository):
    """Concrete memory repository backed by an async SQLAlchemy session."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, memory: Memory) -> Memory:
        """Persist a new memory and return the saved entity."""
        model = MemoryModel(
            id=memory.id,
            user_id=memory.user_id,
            type=memory.type.value,
            content=memory.content,
            importance=memory.importance.value,
            source_message_id=memory.source_message_id,
            is_active=memory.is_active,
            created_at=memory.created_at,
            updated_at=memory.updated_at,
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def find_active_by_user(self, user_id: UUID) -> List[Memory]:
        """Return all active memories for the given user."""
        result = await self.session.execute(
            select(MemoryModel).where(
                MemoryModel.user_id == user_id,
                MemoryModel.is_active == True,  # noqa: E712
            )
        )
        models = result.scalars().all()
        return [self._to_entity(m) for m in models]

    async def find_by_id(self, memory_id: UUID) -> Optional[Memory]:
        """Return the memory with the given ID, or None if not found."""
        result = await self.session.execute(
            select(MemoryModel).where(MemoryModel.id == memory_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def update(self, memory: Memory) -> Memory:
        """Persist changes to an existing memory and return it."""
        result = await self.session.execute(
            select(MemoryModel).where(MemoryModel.id == memory.id)
        )
        model = result.scalar_one_or_none()
        if model is None:
            raise ValueError(f"Memory {memory.id} not found")
        model.type = memory.type.value
        model.content = memory.content
        model.importance = memory.importance.value
        model.is_active = memory.is_active
        model.updated_at = memory.updated_at
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def delete(self, memory_id: UUID) -> bool:
        """Delete the memory with the given ID.

        Returns:
            True if deleted, False if not found.
        """
        result = await self.session.execute(
            select(MemoryModel).where(MemoryModel.id == memory_id)
        )
        model = result.scalar_one_or_none()
        if model is None:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    def _to_entity(self, model: MemoryModel) -> Memory:
        """Convert a MemoryModel ORM instance to a Memory domain entity."""
        return Memory(
            id=model.id,
            user_id=model.user_id,
            type=MemoryType(model.type),
            content=model.content,
            importance=MemoryImportance(model.importance),
            source_message_id=model.source_message_id,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
