"""Azure OpenAI provider adapter implementing ILLMProvider."""

from typing import List, Optional

import openai

from application.interfaces.llm_provider import ILLMProvider, LLMMessage, LLMResponse
from infrastructure.llm_providers.exceptions import RateLimitError, ServiceUnavailableError


class AzureOpenAIProvider(ILLMProvider):
    """LLM provider adapter for the Azure OpenAI Service.

    Uses the async Azure OpenAI client to generate chat completions and
    text embeddings via a customer-managed Azure deployment.
    """

    def __init__(
        self,
        api_key: str,
        endpoint: str,
        deployment_name: str,
        api_version: str = "2023-05-15",
    ) -> None:
        """Initialise the provider.

        Args:
            api_key: Azure OpenAI API key.
            endpoint: Azure OpenAI resource endpoint URL
                (e.g. ``https://<resource>.openai.azure.com/``).
            deployment_name: Name of the Azure deployment to use for both
                completions and embeddings.
            api_version: Azure OpenAI REST API version (default: "2023-05-15").
        """
        self.api_key = api_key
        self.endpoint = endpoint
        self.deployment_name = deployment_name
        self.api_version = api_version

    def _make_client(self) -> openai.AsyncAzureOpenAI:
        """Create and return an AsyncAzureOpenAI client."""
        return openai.AsyncAzureOpenAI(
            api_key=self.api_key,
            azure_endpoint=self.endpoint,
            api_version=self.api_version,
        )

    async def generate_completion(
        self,
        messages: List[LLMMessage],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> LLMResponse:
        """Generate a chat completion using the Azure OpenAI Service.

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
        client = self._make_client()
        openai_messages = [
            {"role": msg.role, "content": msg.content} for msg in messages
        ]

        try:
            response = await client.chat.completions.create(
                model=self.deployment_name,
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

        Uses the configured deployment for embeddings.

        Args:
            text: Input text to embed.

        Returns:
            A list of floats representing the embedding vector.

        Raises:
            RateLimitError: When the API returns a 429 rate-limit response.
            ServiceUnavailableError: When the API is unreachable or returns
                an unexpected error.
        """
        client = self._make_client()

        try:
            response = await client.embeddings.create(
                model=self.deployment_name,
                input=text,
            )
        except openai.RateLimitError as exc:
            raise RateLimitError("Rate limit exceeded, please try again later") from exc
        except (openai.APIConnectionError, openai.APITimeoutError) as exc:
            raise ServiceUnavailableError("AI service temporarily unavailable") from exc
        except openai.APIError as exc:
            raise ServiceUnavailableError("AI service temporarily unavailable") from exc

        return response.data[0].embedding
