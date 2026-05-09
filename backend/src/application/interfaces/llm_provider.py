"""LLM provider interface and associated data types."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class LLMMessage:
    """A single message in the format expected by an LLM provider.

    Attributes:
        role: The speaker role — "system", "user", or "assistant".
        content: The text content of the message.
    """

    role: str
    content: str


@dataclass
class LLMResponse:
    """The response returned by an LLM provider after a completion call.

    Attributes:
        content: The generated text content.
        model: The model identifier used to produce the response.
        usage: Token usage statistics (e.g. prompt_tokens, completion_tokens,
            total_tokens).
        finish_reason: The reason the model stopped generating
            (e.g. "stop", "length").
    """

    content: str
    model: str
    usage: Dict[str, int]
    finish_reason: str


class ILLMProvider(ABC):
    """Abstract interface for LLM provider adapters.

    Concrete implementations (OpenAI, Azure OpenAI, etc.) must implement
    all abstract methods so that the application layer remains decoupled
    from any specific provider SDK.
    """

    @abstractmethod
    async def generate_completion(
        self,
        messages: List[LLMMessage],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> LLMResponse:
        """Generate a chat completion from a list of messages.

        Args:
            messages: Ordered list of messages forming the conversation
                context.
            temperature: Sampling temperature controlling randomness
                (0.0–2.0).
            max_tokens: Optional cap on the number of tokens to generate.

        Returns:
            An LLMResponse containing the generated content and metadata.
        """
        pass

    @abstractmethod
    async def generate_embedding(self, text: str) -> List[float]:
        """Generate an embedding vector for the given text.

        Used for future RAG (Retrieval-Augmented Generation) features.

        Args:
            text: The input text to embed.

        Returns:
            A list of floats representing the embedding vector.
        """
        pass
