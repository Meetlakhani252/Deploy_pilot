"""Authentication router implementing FR-01, Module M1."""
from fastapi import APIRouter, Depends, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.config import settings
from app.core.database import get_db
from app.core.exceptions import RefreshTokenMissingException
from app.models.models import User
from app.schemas.auth import (
    AuthResponse,
    MessageResponse,
    UserLogin,
    UserResponse,
    UserSignUp,
)
from app.services.auth_service import (
    authenticate_user,
    refresh_user_session,
    signup_user,
)

router = APIRouter(tags=["Authentication"])


def _set_refresh_cookie(response: Response, token: str) -> None:
    """Helper to attach httpOnly secure rotating refresh token cookie."""
    response.set_cookie(
        key=settings.COOKIE_NAME,
        value=token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400,
        path="/",
    )


def _clear_refresh_cookie(response: Response) -> None:
    """Helper to clear refresh token cookie upon logout."""
    response.delete_cookie(
        key=settings.COOKIE_NAME,
        path="/",
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
    )


@router.post(
    "/signup",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Sign up a new user",
)
async def signup(
    data: UserSignUp,
    response: Response,
    db: AsyncSession = Depends(get_db),
) -> AuthResponse:
    """Create a new user account with argon2 password hash and return session."""
    user, access_token, refresh_token = await signup_user(db, data)
    _set_refresh_cookie(response, refresh_token)
    return AuthResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse.model_validate(user),
    )


@router.post(
    "/login",
    response_model=AuthResponse,
    summary="Log in user",
)
async def login(
    data: UserLogin,
    response: Response,
    db: AsyncSession = Depends(get_db),
) -> AuthResponse:
    """Authenticate with email and password, enforcing account lockout on repeated failures."""
    user, access_token, refresh_token = await authenticate_user(db, data)
    _set_refresh_cookie(response, refresh_token)
    return AuthResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse.model_validate(user),
    )


@router.post(
    "/refresh",
    response_model=AuthResponse,
    summary="Refresh session and rotate refresh token",
)
async def refresh_token(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
) -> AuthResponse:
    """Rotate refresh token and issue new short-lived access token."""
    token = request.cookies.get(settings.COOKIE_NAME)
    if not token:
        # Check standard cookie name fallback or header
        token = request.cookies.get("refresh_token") or request.headers.get("x-refresh-token")

    if not token:
        raise RefreshTokenMissingException("Refresh token is missing")

    user, new_access_token, new_refresh_token = await refresh_user_session(db, token)
    _set_refresh_cookie(response, new_refresh_token)

    return AuthResponse(
        access_token=new_access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse.model_validate(user),
    )


@router.post(
    "/logout",
    response_model=MessageResponse,
    summary="Log out user",
)
async def logout(
    response: Response,
) -> MessageResponse:
    """Clear refresh token cookie to terminate session."""
    _clear_refresh_cookie(response)
    return MessageResponse(message="Logged out successfully")


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile",
)
async def get_me(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """Get profile of currently authenticated user."""
    return UserResponse.model_validate(current_user)
