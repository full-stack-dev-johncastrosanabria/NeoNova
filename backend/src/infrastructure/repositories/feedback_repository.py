"""SQLAlchemy implementation of IFeedbackRepository."""

from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from application.interfaces.repositories import IFeedbackRepository
from domain.entities.feedback import Feedback
from infrastructure.models.feedback_model import FeedbackModel


class FeedbackRepository(IFeedbackRepository):
    """Concrete feedback repository backed by an async SQLAlchemy session."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, feedback: Feedback) -> Feedback:
        """Persist new feedback and return the saved entity."""
        model = FeedbackModel(
            id=feedback.id,
            message_id=feedback.message_id,
            user_id=feedback.user_id,
            rating=feedback.rating,
            comment=feedback.comment,
            correction=feedback.correction,
            created_at=feedback.created_at,
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def find_by_message(self, message_id: UUID) -> Optional[Feedback]:
        """Return feedback for the given message, or None if not found."""
        result = await self.session.execute(
            select(FeedbackModel).where(FeedbackModel.message_id == message_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    def _to_entity(self, model: FeedbackModel) -> Feedback:
        """Convert a FeedbackModel ORM instance to a Feedback domain entity."""
        return Feedback(
            id=model.id,
            message_id=model.message_id,
            user_id=model.user_id,
            rating=model.rating,
            comment=model.comment,
            correction=model.correction,
            created_at=model.created_at,
        )
