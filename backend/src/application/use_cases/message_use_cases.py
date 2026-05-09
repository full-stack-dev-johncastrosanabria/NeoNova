"""Message use cases for sending and listing messages in a conversation."""

from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from application.dtos.message_dtos import SendMessageDTO
from application.interfaces.llm_provider import ILLMProvider
from application.interfaces.repositories import (
    IConversationRepository,
    IMessageRepository,
)
from application.services.agent_service import AgentService
from application.services.memory_service import MemoryService
from domain.entities.message import Message
from domain.enums import MessageRole


class SendMessageUseCase:
    """Use case for sending a user message and receiving an AI response."""

    def __init__(
        self,
        conversation_repo: IConversationRepository,
        message_repo: IMessageRepository,
        memory_service: MemoryService,
        agent_service: AgentService,
        llm_provider: ILLMProvider,
    ) -> None:
        """Initialise with required dependencies.

        Args:
            conversation_repo: Repository for conversation persistence.
            message_repo: Repository for message persistence.
            memory_service: Service for retrieving active user memories.
            agent_service: Service for building LLM prompts.
            llm_provider: Provider for generating LLM completions.
        """
        self.conversation_repo = conversation_repo
        self.message_repo = message_repo
        self.memory_service = memory_service
        self.agent_service = agent_service
        self.llm_provider = llm_provider

    async def execute(
        self, dto: SendMessageDTO, user_id: UUID
    ) -> tuple[Message, Message]:
        """Send a user message and return both the user and assistant messages.

        Steps:
        1. Verify the conversation exists and belongs to the user.
        2. Retrieve active memories for context.
        3. Retrieve the last 10 messages for conversation history.
        4. Build the LLM prompt with memory and history context.
        5. Generate the AI completion.
        6. Persist the user message.
        7. Persist the assistant message with model metadata.
        8. Update the conversation's updated_at timestamp.

        Args:
            dto: Data transfer object containing conversation_id and content.
            user_id: The UUID of the user sending the message.

        Returns:
            A tuple of (user_message, assistant_message).

        Raises:
            ValueError: If the conversation does not exist or does not
                belong to the requesting user.
        """
        conversation = await self.conversation_repo.find_by_id(
            dto.conversation_id
        )
        if not conversation or conversation.user_id != user_id:
            raise ValueError("Conversation not found")

        memories = await self.memory_service.get_active_memories(user_id)

        recent_messages = await self.message_repo.find_by_conversation(
            dto.conversation_id, limit=10
        )

        prompt_messages = self.agent_service.build_prompt(
            memories, recent_messages, dto.content
        )

        llm_response = await self.llm_provider.generate_completion(
            prompt_messages
        )

        now = datetime.utcnow()

        user_message = Message(
            id=uuid4(),
            conversation_id=dto.conversation_id,
            role=MessageRole.USER,
            content=dto.content,
            metadata_json=None,
            created_at=now,
        )
        user_message = await self.message_repo.create(user_message)

        assistant_message = Message(
            id=uuid4(),
            conversation_id=dto.conversation_id,
            role=MessageRole.ASSISTANT,
            content=llm_response.content,
            metadata_json={
                "model": llm_response.model,
                "usage": llm_response.usage,
            },
            created_at=datetime.utcnow(),
        )
        assistant_message = await self.message_repo.create(assistant_message)

        conversation.updated_at = datetime.utcnow()
        await self.conversation_repo.update(conversation)

        return user_message, assistant_message


class ListMessagesUseCase:
    """Use case for listing all messages in a conversation."""

    def __init__(
        self,
        conversation_repo: IConversationRepository,
        message_repo: IMessageRepository,
    ) -> None:
        """Initialise with required dependencies.

        Args:
            conversation_repo: Repository for conversation persistence.
            message_repo: Repository for message persistence.
        """
        self.conversation_repo = conversation_repo
        self.message_repo = message_repo

    async def execute(
        self, conversation_id: UUID, user_id: UUID
    ) -> List[Message]:
        """Return all messages in a conversation, verifying ownership.

        Args:
            conversation_id: The UUID of the conversation to query.
            user_id: The UUID of the requesting user.

        Returns:
            A list of Message entities ordered by creation time.

        Raises:
            ValueError: If the conversation does not exist or does not
                belong to the requesting user.
        """
        conversation = await self.conversation_repo.find_by_id(
            conversation_id
        )
        if not conversation or conversation.user_id != user_id:
            raise ValueError("Conversation not found")

        return await self.message_repo.find_by_conversation(conversation_id)
