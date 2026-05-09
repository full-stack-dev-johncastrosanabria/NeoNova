"""Factory for creating the configured LLM provider instance."""

from application.interfaces.llm_provider import ILLMProvider
from infrastructure.llm_providers.azure_openai_provider import AzureOpenAIProvider
from infrastructure.llm_providers.openai_provider import OpenAIProvider


def create_llm_provider(settings) -> ILLMProvider:
    """Return the appropriate LLM provider based on application settings.

    Reads ``settings.LLM_PROVIDER`` to decide which concrete adapter to
    instantiate.  Any value other than ``"azure"`` (case-insensitive) falls
    back to the standard OpenAI provider.

    Args:
        settings: Application settings object (e.g. an instance of
            ``application.config.Settings``).

    Returns:
        A concrete :class:`ILLMProvider` implementation ready for use.
    """
    if settings.LLM_PROVIDER.lower() == "azure":
        return AzureOpenAIProvider(
            api_key=settings.AZURE_OPENAI_API_KEY,
            endpoint=settings.AZURE_OPENAI_ENDPOINT,
            deployment_name=settings.AZURE_OPENAI_DEPLOYMENT_NAME,
            api_version=settings.AZURE_OPENAI_API_VERSION,
        )

    return OpenAIProvider(
        api_key=settings.OPENAI_API_KEY,
        model=settings.OPENAI_MODEL,
    )
