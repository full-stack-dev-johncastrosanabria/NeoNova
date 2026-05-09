"""Conversation use cases for creating, listing, and deleting conversations."""

from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from application.interfaces.repositories import IConversationRepository
from domain.entities.conversation import Conversation


class CreateConversationUseCase:
    """Use case for creating a new conversation."""

    def __init__(
        self,
        conversation_repo: IConversationRepository,
    ) -> None:
        """Initialise with required dependencies.

        Args:
            conversation_repo: Repository for conversation persistence.
        """
        self.conversation_repo = conversation_repo

    async def execute(self, title: str, user_id: UUID) -> Conversation:
        """Create a new conversation for the given user.

        Args:
            title: The title for the new conversation.
            user_id: The UUID of the user who owns the conversation.

        Returns:
            The newly created and persisted Conversation entity.

        Raises:
            ValueError: If the title is empty.
        """
        if not title or not title.strip():
            raise ValueError("Conversation title cannot be empty")

        now = datetime.utcnow()
        conversation = Conversation(
            id=uuid4(),
            user_id=user_id,
            title=title,
            created_at=now,
            updated_at=now,
        )

        return await self.conversation_repo.create(conversation)


class ListConversationsUseCase:
    """Use case for listing all conversations belonging to a user."""

    def __init__(
        self,
        conversation_repo: IConversationRepository,
    ) -> None:
        """Initialise with required dependencies.

        Args:
            conversation_repo: Repository for conversation persistence.
        """
        self.conversation_repo = conversation_repo

    async def execute(self, user_id: UUID) -> List[Conversation]:
        """Return all conversations for the given user.

        Args:
            user_id: The UUID of the user whose conversations to retrieve.

        Returns:
            A list of Conversation entities belonging to the user.
        """
        return await self.conversation_repo.find_by_user(user_id)


class DeleteConversationUseCase:
    """Use case for deleting a conversation owned by a user."""

    def __init__(
        self,
        conversation_repo: IConversationRepository,
    ) -> None:
        """Initialise with required dependencies.

        Args:
            conversation_repo: Repository for conversation persistence.
        """
        self.conversation_repo = conversation_repo

    async def execute(
        self, conversation_id: UUID, user_id: UUID
    ) -> bool:
        """Delete a conversation, verifying ownership first.

        Args:
            conversation_id: The UUID of the conversation to delete.
            user_id: The UUID of the requesting user.

        Returns:
            True if the conversation was successfully deleted.

        Raises:
            ValueError: If the conversation does not exist or does not
                belong to the requesting user.
        """
        conversation = await self.conversation_repo.find_by_id(
            conversation_id
        )
        if not conversation or conversation.user_id != user_id:
            raise ValueError("Conversation not found")

        return await self.conversation_repo.delete(conversation_id)
