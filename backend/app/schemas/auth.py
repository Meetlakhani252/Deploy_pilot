"""Pydantic schemas for Authentication and User management."""

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserSignUp(BaseModel):
    """User registration payload."""

    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")


class UserLogin(BaseModel):
    """User login payload."""

    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """User profile response."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: str
    created_at: datetime
    last_login_at: datetime | None = None
    failed_logins: int = 0
    locked_until: datetime | None = None


class AuthResponse(BaseModel):
    """Successful authentication response."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int = 900  # 15 minutes (in seconds)
    user: UserResponse


class MessageResponse(BaseModel):
    """Generic message response."""

    message: str


class ErrorDetail(BaseModel):
    """Standard error response format matching TSD Section 6."""

    code: str
    message: str
    details: Any | None = None
