"""Feedback use cases for creating feedback on assistant messages."""

from datetime import datetime
from uuid import UUID, uuid4

from application.dtos.feedback_dtos import CreateFeedbackDTO
from application.interfaces.repositories import (
    IFeedbackRepository,
    IMessageRepository,
)
from application.services.memory_service import MemoryService
from domain.entities.feedback import Feedback


class CreateFeedbackUseCase:
    """Use case for submitting feedback on an assistant message."""

    def __init__(
        self,
        message_repo: IMessageRepository,
        feedback_repo: IFeedbackRepository,
        memory_service: MemoryService,
    ) -> None:
        """Initialise with required dependencies.

        Args:
            message_repo: Repository for message persistence.
            feedback_repo: Repository for feedback persistence.
            memory_service: Service used to extract memories from corrections.
        """
        self.message_repo = message_repo
        self.feedback_repo = feedback_repo
        self.memory_service = memory_service

    async def execute(
        self, dto: CreateFeedbackDTO, user_id: UUID
    ) -> Feedback:
        """Create feedback for a message, optionally extracting a memory.

        Steps:
        1. Verify the target message exists.
        2. Check that no feedback already exists for the message.
        3. Create and persist the Feedback entity.
        4. If a correction is provided, extract a memory from it.

        Args:
            dto: Data transfer object containing feedback details.
            user_id: The UUID of the user submitting the feedback.

        Returns:
            The newly created and persisted Feedback entity.

        Raises:
            ValueError: If the message is not found or feedback already
                exists for the message.
        """
        message = await self.message_repo.find_by_id(dto.message_id)
        if not message:
            raise ValueError("Message not found")

        existing_feedback = await self.feedback_repo.find_by_message(
            dto.message_id
        )
        if existing_feedback:
            raise ValueError("Feedback already exists for this message")

        feedback = Feedback(
            id=uuid4(),
            message_id=dto.message_id,
            user_id=user_id,
            rating=dto.rating,
            comment=dto.comment,
            correction=dto.correction,
            created_at=datetime.utcnow(),
        )
        feedback = await self.feedback_repo.create(feedback)

        if dto.correction:
            await self.memory_service.extract_memory_from_correction(
                dto.correction, dto.message_id, user_id
            )

        return feedback
