"""Pydantic schemas for feedback endpoints."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class FeedbackRequest(BaseModel):
    """Request schema for submitting feedback on a message."""

    message_id: UUID
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = None
    correction: Optional[str] = None


class FeedbackResponse(BaseModel):
    """Response schema representing feedback."""

    id: UUID
    message_id: UUID
    rating: Optional[int] = None
    comment: Optional[str] = None
    correction: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
