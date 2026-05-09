"""Pydantic schemas for memory endpoints."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class MemoryRequest(BaseModel):
    """Request schema for creating a memory."""

    type: str
    content: str = Field(min_length=1)
    importance: int = Field(ge=1, le=4)


class MemoryResponse(BaseModel):
    """Response schema representing a memory."""

    id: UUID
    user_id: UUID
    type: str
    content: str
    importance: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
