"""Custom exceptions for LLM provider errors."""


class RateLimitError(Exception):
    """Raised when the LLM provider returns a rate limit error."""
    pass


class ServiceUnavailableError(Exception):
    """Raised when the LLM provider is temporarily unavailable."""
    pass
