"""SQLAlchemy implementation of IMessageRepository."""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from application.interfaces.repositories import IMessageRepository
from domain.entities.message import Message
from domain.enums import MessageRole
from infrastructure.models.message_model import MessageModel


class MessageRepository(IMessageRepository):
    """Concrete message repository backed by an async SQLAlchemy session."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, message: Message) -> Message:
        """Persist a new message and return the saved entity."""
        model = MessageModel(
            id=message.id,
            conversation_id=message.conversation_id,
            role=message.role.value,
            content=message.content,
            metadata_json=message.metadata_json,
            created_at=message.created_at,
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def find_by_id(self, message_id: UUID) -> Optional[Message]:
        """Return the message with the given ID, or None if not found."""
        result = await self.session.execute(
            select(MessageModel).where(MessageModel.id == message_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def find_by_conversation(
        self,
        conversation_id: UUID,
        limit: Optional[int] = None,
    ) -> List[Message]:
        """Return messages for the given conversation in ascending order.

        Queries in descending order (newest first) with an optional limit,
        then reverses the result to return messages in ascending (chronological)
        order.
        """
        query = (
            select(MessageModel)
            .where(MessageModel.conversation_id == conversation_id)
            .order_by(MessageModel.created_at.desc())
        )
        if limit is not None:
            query = query.limit(limit)
        result = await self.session.execute(query)
        models = result.scalars().all()
        # Reverse to restore ascending (chronological) order
        return [self._to_entity(m) for m in reversed(models)]

    def _to_entity(self, model: MessageModel) -> Message:
        """Convert a MessageModel ORM instance to a Message domain entity."""
        return Message(
            id=model.id,
            conversation_id=model.conversation_id,
            role=MessageRole(model.role),
            content=model.content,
            metadata_json=model.metadata_json,
            created_at=model.created_at,
        )
