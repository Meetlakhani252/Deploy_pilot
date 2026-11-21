"""Dependencies for FastAPI endpoints."""

import uuid
from datetime import UTC, datetime

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.exceptions import AccountLockedException, UnauthorizedException
from app.core.security import decode_token
from app.models.models import User

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
    auto_error=False,
)


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str | None = Depends(oauth2_scheme),
) -> User:
    """Retrieve current authenticated user from Bearer access token."""
    if not token:
        raise UnauthorizedException("Authentication required")

    payload = decode_token(token, expected_type="access")
    user_id_str = payload.get("sub")
    if not user_id_str:
        raise UnauthorizedException("Invalid token credentials")

    try:
        user_id = uuid.UUID(user_id_str)
    except ValueError as e:
        raise UnauthorizedException("Invalid token credentials") from e

    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None:
        raise UnauthorizedException("User not found")

    now = datetime.now(UTC)
    if user.locked_until and user.locked_until > now:
        remaining_seconds = int((user.locked_until - now).total_seconds())
        minutes_remaining = max(1, (remaining_seconds + 59) // 60)
        raise AccountLockedException(
            minutes_remaining=minutes_remaining,
            locked_until_iso=user.locked_until.isoformat(),
        )

    return user
