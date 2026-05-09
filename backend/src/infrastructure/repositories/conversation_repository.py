"""SQLAlchemy implementation of IConversationRepository."""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from application.interfaces.repositories import IConversationRepository
from domain.entities.conversation import Conversation
from infrastructure.models.conversation_model import ConversationModel


class ConversationRepository(IConversationRepository):
    """Concrete conversation repository backed by an async SQLAlchemy session."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, conversation: Conversation) -> Conversation:
        """Persist a new conversation and return the saved entity."""
        model = ConversationModel(
            id=conversation.id,
            user_id=conversation.user_id,
            title=conversation.title,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at,
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def find_by_id(self, conversation_id: UUID) -> Optional[Conversation]:
        """Return the conversation with the given ID, or None if not found."""
        result = await self.session.execute(
            select(ConversationModel).where(ConversationModel.id == conversation_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def find_by_user(self, user_id: UUID) -> List[Conversation]:
        """Return all conversations for the given user, ordered by updated_at descending."""
        result = await self.session.execute(
            select(ConversationModel)
            .where(ConversationModel.user_id == user_id)
            .order_by(ConversationModel.updated_at.desc())
        )
        models = result.scalars().all()
        return [self._to_entity(m) for m in models]

    async def update(self, conversation: Conversation) -> Conversation:
        """Persist changes to an existing conversation and return it."""
        result = await self.session.execute(
            select(ConversationModel).where(ConversationModel.id == conversation.id)
        )
        model = result.scalar_one_or_none()
        if model is None:
            raise ValueError(f"Conversation {conversation.id} not found")
        model.title = conversation.title
        model.updated_at = conversation.updated_at
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def delete(self, conversation_id: UUID) -> bool:
        """Delete the conversation with the given ID.

        Returns:
            True if deleted, False if not found.
        """
        result = await self.session.execute(
            select(ConversationModel).where(ConversationModel.id == conversation_id)
        )
        model = result.scalar_one_or_none()
        if model is None:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    def _to_entity(self, model: ConversationModel) -> Conversation:
        """Convert a ConversationModel ORM instance to a Conversation domain entity."""
        return Conversation(
            id=model.id,
            user_id=model.user_id,
            title=model.title,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
