"""Factory for creating the configured LLM provider instance."""

from application.interfaces.llm_provider import ILLMProvider
from infrastructure.llm_providers.azure_openai_provider import AzureOpenAIProvider
from infrastructure.llm_providers.mock_provider import MockLLMProvider
from infrastructure.llm_providers.openai_provider import OpenAIProvider


def create_llm_provider(settings) -> ILLMProvider:
    """Return the appropriate LLM provider based on application settings.

    Reads ``settings.LLM_PROVIDER`` to decide which concrete adapter to
    instantiate.  Any value other than ``"azure"`` (case-insensitive) falls
    back to the standard OpenAI provider.

    If the API key is not configured (placeholder value), returns a mock
    provider for development/testing.

    Args:
        settings: Application settings object (e.g. an instance of
            ``application.config.Settings``).

    Returns:
        A concrete :class:`ILLMProvider` implementation ready for use.
    """
    # Check if using Azure OpenAI
    if settings.LLM_PROVIDER.lower() == "azure":
        # Check if Azure API key is configured
        if not settings.AZURE_OPENAI_API_KEY or settings.AZURE_OPENAI_API_KEY.startswith("your-"):
            return MockLLMProvider(model="mock-azure-gpt-4")
        return AzureOpenAIProvider(
            api_key=settings.AZURE_OPENAI_API_KEY,
            endpoint=settings.AZURE_OPENAI_ENDPOINT,
            deployment_name=settings.AZURE_OPENAI_DEPLOYMENT_NAME,
            api_version=settings.AZURE_OPENAI_API_VERSION,
        )

    # Check if OpenAI API key is configured
    if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY.startswith("sk-your-"):
        return MockLLMProvider(model="mock-gpt-4")

    return OpenAIProvider(
        api_key=settings.OPENAI_API_KEY,
        model=settings.OPENAI_MODEL,
    )
