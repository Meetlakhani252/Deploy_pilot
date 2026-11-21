"""Authentication service handling business logic, lockout logic and session rotation."""
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import (
    AccountLockedException,
    InvalidCredentialsException,
    InvalidTokenException,
    UserAlreadyExistsException,
)
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.models.models import AuditLog, Setting, User
from app.schemas.auth import UserLogin, UserSignUp


async def signup_user(db: AsyncSession, data: UserSignUp) -> tuple[User, str, str]:
    """Register a new user, initialize user settings, and return user with access & refresh tokens."""
    normalized_email = data.email.strip().lower()

    # Check for existing user
    stmt = select(User).where(User.email == normalized_email)
    result = await db.execute(stmt)
    existing_user = result.scalar_one_or_none()
    if existing_user is not None:
        raise UserAlreadyExistsException("An account with this email already exists")

    hashed_pw = hash_password(data.password)
    user_id = uuid.uuid4()
    now = datetime.now(timezone.utc)

    user = User(
        id=user_id,
        email=normalized_email,
        password_hash=hashed_pw,
        created_at=now,
        last_login_at=now,
        failed_logins=0,
        locked_until=None,
    )
    db.add(user)

    # Initialize default settings for user
    user_setting = Setting(
        user_id=user_id,
        llm_provider="gemini",
        llm_model="gemini-1.5-pro",
        email_enabled=None,
    )
    db.add(user_setting)

    # Record audit log
    audit_log = AuditLog(
        user_id=user_id,
        event_type="auth.signup",
        entity_type="user",
        entity_id=str(user_id),
        details={"email": normalized_email},
        ts=now,
    )
    db.add(audit_log)

    await db.commit()
    await db.refresh(user)

    access_token = create_access_token(user_id=user.id, email=user.email)
    refresh_token = create_refresh_token(user_id=user.id, email=user.email)

    return user, access_token, refresh_token


async def authenticate_user(db: AsyncSession, data: UserLogin) -> tuple[User, str, str]:
    """Authenticate a user, enforcing 5-failed-in-10-min lockout logic and rotating tokens."""
    normalized_email = data.email.strip().lower()
    now = datetime.now(timezone.utc)

    stmt = select(User).where(User.email == normalized_email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None:
        # Dummy verification to mitigate timing attacks
        verify_password(data.password, "$argon2id$v=19$m=65536,t=3,p=4$dummyhashdummyhash$dummyhashdummyhash")
        raise InvalidCredentialsException("Invalid email or password")

    # Check existing lockout state
    if user.locked_until is not None:
        if user.locked_until > now:
            remaining_seconds = int((user.locked_until - now).total_seconds())
            minutes_remaining = max(1, (remaining_seconds + 59) // 60)
            raise AccountLockedException(
                minutes_remaining=minutes_remaining,
                locked_until_iso=user.locked_until.isoformat(),
            )
        else:
            # Lockout period expired: reset lock
            user.locked_until = None
            user.failed_logins = 0

    # Verify password with argon2
    if verify_password(data.password, user.password_hash):
        # Successful login
        user.failed_logins = 0
        user.locked_until = None
        user.last_login_at = now

        audit_entry = AuditLog(
            user_id=user.id,
            event_type="auth.login_success",
            entity_type="user",
            entity_id=str(user.id),
            details={"email": user.email},
            ts=now,
        )
        db.add(audit_entry)
        await db.commit()
        await db.refresh(user)

        access_token = create_access_token(user_id=user.id, email=user.email)
        refresh_token = create_refresh_token(user_id=user.id, email=user.email)
        return user, access_token, refresh_token

    # Failed password attempt: calculate failures within window (10 min)
    window_start = now - timedelta(minutes=settings.LOCKOUT_WINDOW_MINUTES)
    count_stmt = select(func.count(AuditLog.id)).where(
        AuditLog.user_id == user.id,
        AuditLog.event_type == "auth.login_failed",
        AuditLog.ts >= window_start,
    )
    count_result = await db.execute(count_stmt)
    recent_failed_count = (count_result.scalar() or 0) + 1  # include this attempt
    user.failed_logins = recent_failed_count

    is_locked = False
    if recent_failures := recent_failed_count >= settings.LOCKOUT_THRESHOLD:
        user.locked_until = now + timedelta(minutes=settings.LOCKOUT_DURATION_MINUTES)
        is_locked = True

    audit_entry = AuditLog(
        user_id=user.id,
        event_type="auth.login_failed",
        entity_type="user",
        entity_id=str(user.id),
        details={
            "email": user.email,
            "failed_attempts": recent_failed_count,
            "locked": is_locked,
        },
        ts=now,
    )
    db.add(audit_entry)
    await db.commit()

    if is_locked:
        raise AccountLockedException(
            minutes_remaining=settings.LOCKOUT_DURATION_MINUTES,
            locked_until_iso=user.locked_until.isoformat() if user.locked_until else None,
        )

    attempts_left = max(0, settings.LOCKOUT_THRESHOLD - recent_failed_count)
    raise InvalidCredentialsException(
        message="Invalid email or password",
        details={"attempts_remaining": attempts_left},
    )


async def refresh_user_session(db: AsyncSession, refresh_token: str) -> tuple[User, str, str]:
    """Validate refresh token and rotate with new access & refresh tokens."""
    payload = decode_token(refresh_token, expected_type="refresh")
    user_id_str = payload.get("sub")
    if not user_id_str:
        raise InvalidTokenException("Invalid token payload")

    try:
        user_id = uuid.UUID(user_id_str)
    except ValueError as e:
        raise InvalidTokenException("Invalid user id in token") from e

    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None:
        raise InvalidTokenException("User does not exist")

    now = datetime.now(timezone.utc)
    if user.locked_until and user.locked_until > now:
        remaining_seconds = int((user.locked_until - now).total_seconds())
        minutes_remaining = max(1, (remaining_seconds + 59) // 60)
        raise AccountLockedException(
            minutes_remaining=minutes_remaining,
            locked_until_iso=user.locked_until.isoformat(),
        )

    # Rotating refresh token: issue new pair
    new_access_token = create_access_token(user_id=user.id, email=user.email)
    new_refresh_token = create_refresh_token(user_id=user.id, email=user.email)

    audit_entry = AuditLog(
        user_id=user.id,
        event_type="auth.refresh",
        entity_type="user",
        entity_id=str(user.id),
        details={"email": user.email},
        ts=now,
    )
    db.add(audit_entry)
    await db.commit()

    return user, new_access_token, new_refresh_token
