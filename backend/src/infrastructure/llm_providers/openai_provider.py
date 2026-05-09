"""OpenAI provider adapter implementing ILLMProvider."""

from typing import List, Optional

import openai

from application.interfaces.llm_provider import ILLMProvider, LLMMessage, LLMResponse
from infrastructure.llm_providers.exceptions import RateLimitError, ServiceUnavailableError


class OpenAIProvider(ILLMProvider):
    """LLM provider adapter for the OpenAI API.

    Uses the async OpenAI client to generate chat completions and
    text embeddings.
    """

    def __init__(self, api_key: str, model: str = "gpt-4") -> None:
        """Initialise the provider.

        Args:
            api_key: OpenAI API key.
            model: Chat model identifier (default: "gpt-4").
        """
        self.api_key = api_key
        self.model = model

    async def generate_completion(
        self,
        messages: List[LLMMessage],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> LLMResponse:
        """Generate a chat completion using the OpenAI API.

        Args:
            messages: Ordered list of LLMMessage objects.
            temperature: Sampling temperature (0.0–2.0).
            max_tokens: Optional maximum number of tokens to generate.

        Returns:
            LLMResponse with the generated content and usage metadata.

        Raises:
            RateLimitError: When the API returns a 429 rate-limit response.
            ServiceUnavailableError: When the API is unreachable or returns
                an unexpected error.
        """
        client = openai.AsyncOpenAI(api_key=self.api_key)
        openai_messages = [
            {"role": msg.role, "content": msg.content} for msg in messages
        ]

        try:
            response = await client.chat.completions.create(
                model=self.model,
                messages=openai_messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        except openai.RateLimitError as exc:
            raise RateLimitError("Rate limit exceeded, please try again later") from exc
        except (openai.APIConnectionError, openai.APITimeoutError) as exc:
            raise ServiceUnavailableError("AI service temporarily unavailable") from exc
        except openai.APIError as exc:
            raise ServiceUnavailableError("AI service temporarily unavailable") from exc

        return LLMResponse(
            content=response.choices[0].message.content,
            model=response.model,
            usage={
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            },
            finish_reason=response.choices[0].finish_reason,
        )

    async def generate_embedding(self, text: str) -> List[float]:
        """Generate an embedding vector for the given text.

        Uses the ``text-embedding-ada-002`` model.

        Args:
            text: Input text to embed.

        Returns:
            A list of floats representing the embedding vector.

        Raises:
            RateLimitError: When the API returns a 429 rate-limit response.
            ServiceUnavailableError: When the API is unreachable or returns
                an unexpected error.
        """
        client = openai.AsyncOpenAI(api_key=self.api_key)

        try:
            response = await client.embeddings.create(
                model="text-embedding-ada-002",
                input=text,
            )
        except openai.RateLimitError as exc:
            raise RateLimitError("Rate limit exceeded, please try again later") from exc
        except (openai.APIConnectionError, openai.APITimeoutError) as exc:
            raise ServiceUnavailableError("AI service temporarily unavailable") from exc
        except openai.APIError as exc:
            raise ServiceUnavailableError("AI service temporarily unavailable") from exc

        return response.data[0].embedding
