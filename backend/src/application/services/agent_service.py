"""Agent service for building LLM prompts with contextual memory."""

from typing import List

from application.interfaces.llm_provider import LLMMessage
from domain.entities.memory import Memory
from domain.entities.message import Message


class AgentService:
    """Service for agent orchestration and prompt construction."""

    SYSTEM_PROMPT = (
        "You're NeoNova, a personal AI assistant designed to help the user "
        "think, plan, learn, build software, analyze documents, and execute "
        "safe tasks. You are practical, clear, and action-oriented. You "
        "remember useful long-term preferences only when appropriate, use "
        "available context carefully, and ask for confirmation before "
        "sensitive actions. You do not pretend to know things you do not know."
    )

    def build_prompt(
        self,
        memories: List[Memory],
        messages: List[Message],
        user_content: str,
    ) -> List[LLMMessage]:
        """Assemble a complete prompt list for the LLM.

        The prompt is composed of:
        1. A system message containing the NeoNova persona and, when present,
           a formatted block of the user's active memories.
        2. Up to the last 10 messages from the conversation history.
        3. The current user message.

        Args:
            memories: Active memories for the user, pre-sorted by importance.
            messages: Full conversation history (only the last 10 are used).
            user_content: The new message text from the user.

        Returns:
            An ordered list of LLMMessage objects ready to send to the
            provider.
        """
        system_content = self.SYSTEM_PROMPT

        if memories:
            memory_context = self._format_memories(memories)
            system_content += f"\n\n## User Context\n{memory_context}"

        prompt_messages: List[LLMMessage] = [
            LLMMessage(role="system", content=system_content)
        ]

        for msg in messages[-10:]:
            prompt_messages.append(
                LLMMessage(role=msg.role.value, content=msg.content)
            )

        prompt_messages.append(LLMMessage(role="user", content=user_content))

        return prompt_messages

    def _format_memories(self, memories: List[Memory]) -> str:
        """Format the top 5 memories as a bullet list for the system prompt.

        Args:
            memories: The memories to format (only the first 5 are used).

        Returns:
            A newline-joined string of formatted memory lines.
        """
        lines = [
            f"- [{memory.type.value}] {memory.content}"
            for memory in memories[:5]
        ]
        return "\n".join(lines)
