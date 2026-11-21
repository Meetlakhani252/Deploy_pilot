"""Schemas package init."""

from app.schemas.auth import (
    AuthResponse,
    ErrorDetail,
    MessageResponse,
    UserLogin,
    UserResponse,
    UserSignUp,
)

__all__ = [
    "AuthResponse",
    "ErrorDetail",
    "MessageResponse",
    "UserLogin",
    "UserResponse",
    "UserSignUp",
]
