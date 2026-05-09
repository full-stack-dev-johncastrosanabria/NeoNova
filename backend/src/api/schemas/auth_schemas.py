"""Pydantic schemas for authentication endpoints."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterRequest(BaseModel):
    """Request schema for user registration."""

    email: EmailStr
    password: str = Field(min_length=8, max_length=72)
    display_name: str = Field(min_length=1)


class LoginRequest(BaseModel):
    """Request schema for user login."""

    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Response schema representing a user."""

    id: UUID
    email: str
    display_name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LoginResponse(BaseModel):
    """Response schema for a successful login."""

    token: str
    user: UserResponse
