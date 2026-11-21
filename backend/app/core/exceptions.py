"""Standard application exceptions and error structures according to TSD Section 6."""
from typing import Any
from fastapi import HTTPException, status


class AppException(HTTPException):
    """Base application exception returning standard error structure: code, message, details."""

    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        details: Any | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=message, headers=headers)
        self.code = code
        self.message = message
        self.details = details


class InvalidCredentialsException(AppException):
    def __init__(self, message: str = "Invalid email or password", details: Any | None = None) -> None:
        super().__init__(
            code="INVALID_CREDENTIALS",
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            details=details,
            headers={"WWW-Authenticate": "Bearer"},
        )


class AccountLockedException(AppException):
    def __init__(
        self,
        minutes_remaining: int = 15,
        locked_until_iso: str | None = None,
    ) -> None:
        super().__init__(
            code="ACCOUNT_LOCKED",
            message=f"Account is locked due to 5 failed login attempts in 10 minutes. Please try again in {minutes_remaining} minutes.",
            status_code=status.HTTP_423_LOCKED,
            details={
                "locked_until": locked_until_iso,
                "minutes_remaining": minutes_remaining,
            },
        )


class UserAlreadyExistsException(AppException):
    def __init__(self, message: str = "An account with this email already exists") -> None:
        super().__init__(
            code="USER_ALREADY_EXISTS",
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class UnauthorizedException(AppException):
    def __init__(self, message: str = "Authentication credentials were not provided or are invalid") -> None:
        super().__init__(
            code="UNAUTHORIZED",
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
        )


class InvalidTokenException(AppException):
    def __init__(self, message: str = "Token is invalid or expired") -> None:
        super().__init__(
            code="INVALID_TOKEN",
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
        )


class RefreshTokenMissingException(AppException):
    def __init__(self, message: str = "Refresh token is missing") -> None:
        super().__init__(
            code="REFRESH_TOKEN_MISSING",
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
