"""Pydantic schemas for error responses."""

from typing import Any, Dict, Optional

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Standard error response schema."""

    error: str
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: str
