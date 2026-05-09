"""Mock LLM provider for development and testing without API keys."""

from typing import List, Optional

from application.interfaces.llm_provider import ILLMProvider, LLMMessage, LLMResponse


class MockLLMProvider(ILLMProvider):
    """Mock LLM provider that returns simulated responses.

    Useful for development and testing when no API key is available.
    """

    def __init__(self, model: str = "mock-gpt-4") -> None:
        """Initialise the mock provider.

        Args:
            model: Model identifier (default: "mock-gpt-4").
        """
        self.model = model

    async def generate_completion(
        self,
        messages: List[LLMMessage],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> LLMResponse:
        """Generate a mock chat completion.

        Args:
            messages: Ordered list of LLMMessage objects.
            temperature: Sampling temperature (ignored in mock).
            max_tokens: Optional maximum number of tokens (ignored in mock).

        Returns:
            LLMResponse with a simulated response.
        """
        # Extract the last user message for context
        user_content = ""
        for msg in reversed(messages):
            if msg.role == "user":
                user_content = msg.content
                break

        # Generate a mock response based on the user message
        mock_responses = {
            "hola": "¡Hola! Soy NeoNova, tu asistente de IA. ¿Cómo puedo ayudarte hoy?",
            "hello": "Hello! I'm NeoNova, your AI assistant. How can I help you today?",
            "hi": "Hi there! I'm NeoNova. What can I do for you?",
        }

        # Check for exact matches (case-insensitive)
        response_content = mock_responses.get(
            user_content.lower().strip(),
            f"Mock response to: {user_content[:50]}... (This is a mock provider - configure OPENAI_API_KEY for real responses)",
        )

        return LLMResponse(
            content=response_content,
            model=self.model,
            usage={
                "prompt_tokens": len(user_content.split()),
                "completion_tokens": len(response_content.split()),
                "total_tokens": len(user_content.split()) + len(response_content.split()),
            },
            finish_reason="stop",
        )

    async def generate_embedding(self, text: str) -> List[float]:
        """Generate a mock embedding vector.

        Args:
            text: Input text to embed.

        Returns:
            A list of 1536 floats (simulating text-embedding-ada-002).
        """
        # Generate a deterministic mock embedding based on text length
        # In a real scenario, this would be a proper embedding
        import hashlib

        hash_obj = hashlib.md5(text.encode())
        hash_int = int(hash_obj.hexdigest(), 16)

        # Generate 1536 floats (ada-002 embedding size)
        embedding = []
        for i in range(1536):
            # Use hash to generate pseudo-random but deterministic values
            value = ((hash_int + i) % 10000) / 10000.0 - 0.5
            embedding.append(value)

        return embedding
