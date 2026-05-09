"""Pydantic schemas for conversation and message endpoints."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ConversationRequest(BaseModel):
    """Request schema for creating a conversation."""

    title: str = Field(min_length=1)


class ConversationResponse(BaseModel):
    """Response schema representing a conversation."""

    id: UUID
    user_id: UUID
    title: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MessageRequest(BaseModel):
    """Request schema for sending a message."""

    content: str = Field(min_length=1)


class MessageResponse(BaseModel):
    """Response schema representing a message."""

    id: UUID
    conversation_id: UUID
    role: str
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
