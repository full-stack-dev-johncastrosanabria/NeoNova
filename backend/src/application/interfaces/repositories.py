"""Abstract repository interfaces for the application layer."""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from domain.entities.conversation import Conversation
from domain.entities.feedback import Feedback
from domain.entities.memory import Memory
from domain.entities.message import Message
from domain.entities.user import User


class IUserRepository(ABC):
    """Abstract interface for user persistence operations."""

    @abstractmethod
    async def create(self, user: User) -> User:
        """Persist a new user and return the saved entity."""
        pass

    @abstractmethod
    async def find_by_id(self, user_id: UUID) -> Optional[User]:
        """Return the user with the given ID, or None if not found."""
        pass

    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[User]:
        """Return the user with the given email, or None if not found."""
        pass


class IConversationRepository(ABC):
    """Abstract interface for conversation persistence operations."""

    @abstractmethod
    async def create(self, conversation: Conversation) -> Conversation:
        """Persist a new conversation and return the saved entity."""
        pass

    @abstractmethod
    async def find_by_id(
        self, conversation_id: UUID
    ) -> Optional[Conversation]:
        """Return the conversation with the given ID, or None if not found."""
        pass

    @abstractmethod
    async def find_by_user(self, user_id: UUID) -> List[Conversation]:
        """Return all conversations belonging to the given user."""
        pass

    @abstractmethod
    async def update(self, conversation: Conversation) -> Conversation:
        """Persist changes to an existing conversation and return it."""
        pass

    @abstractmethod
    async def delete(self, conversation_id: UUID) -> bool:
        """Delete the conversation with the given ID.

        Returns:
            True if the conversation was deleted, False if not found.
        """
        pass


class IMessageRepository(ABC):
    """Abstract interface for message persistence operations."""

    @abstractmethod
    async def create(self, message: Message) -> Message:
        """Persist a new message and return the saved entity."""
        pass

    @abstractmethod
    async def find_by_id(self, message_id: UUID) -> Optional[Message]:
        """Return the message with the given ID, or None if not found."""
        pass

    @abstractmethod
    async def find_by_conversation(
        self,
        conversation_id: UUID,
        limit: Optional[int] = None,
    ) -> List[Message]:
        """Return messages for the given conversation.

        Args:
            conversation_id: The conversation to query.
            limit: Optional maximum number of messages to return.

        Returns:
            List of messages ordered by creation time (ascending).
        """
        pass


class IMemoryRepository(ABC):
    """Abstract interface for memory persistence operations."""

    @abstractmethod
    async def create(self, memory: Memory) -> Memory:
        """Persist a new memory and return the saved entity."""
        pass

    @abstractmethod
    async def find_active_by_user(self, user_id: UUID) -> List[Memory]:
        """Return all active memories for the given user."""
        pass

    @abstractmethod
    async def find_by_id(self, memory_id: UUID) -> Optional[Memory]:
        """Return the memory with the given ID, or None if not found."""
        pass

    @abstractmethod
    async def update(self, memory: Memory) -> Memory:
        """Persist changes to an existing memory and return it."""
        pass

    @abstractmethod
    async def delete(self, memory_id: UUID) -> bool:
        """Delete the memory with the given ID.

        Returns:
            True if the memory was deleted, False if not found.
        """
        pass


class IFeedbackRepository(ABC):
    """Abstract interface for feedback persistence operations."""

    @abstractmethod
    async def create(self, feedback: Feedback) -> Feedback:
        """Persist new feedback and return the saved entity."""
        pass

    @abstractmethod
    async def find_by_message(
        self, message_id: UUID
    ) -> Optional[Feedback]:
        """Return feedback for the given message, or None if not found."""
        pass
