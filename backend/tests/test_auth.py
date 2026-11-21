"""Tests for User Authentication, Argon2 hashing, Lockout logic, and Sessions (FR-01, M1)."""

import uuid
from datetime import UTC, datetime, timedelta

import pytest
from httpx import AsyncClient

from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from tests.conftest import InMemoryAsyncSession

# ---------------------------------------------------------------------------
# 1. Password Hashing & Security Unit Tests
# ---------------------------------------------------------------------------


def test_argon2_password_hashing():
    """Verify password hashing with argon2-cffi."""
    plain = "SuperSecretP@ssword123!"
    hashed = hash_password(plain)

    # Must be valid argon2id hash format
    assert hashed.startswith("$argon2id$")
    assert verify_password(plain, hashed) is True
    assert verify_password("WrongPassword!", hashed) is False
    assert verify_password("", hashed) is False


def test_jwt_token_claims_and_expiration():
    """Verify short-lived access token (15 min) and refresh token generation."""
    user_id = uuid.uuid4()
    email = "developer@deploypilot.com"

    # Access Token (short-lived 15 min)
    access_token = create_access_token(user_id=user_id, email=email)
    payload = decode_token(access_token, expected_type="access")
    assert payload["sub"] == str(user_id)
    assert payload["email"] == email
    assert payload["type"] == "access"
    assert "jti" in payload
    # Expiration is ~15 minutes
    duration = payload["exp"] - payload["iat"]
    assert 890 <= duration <= 910

    # Refresh Token (7 days)
    refresh_token = create_refresh_token(user_id=user_id, email=email)
    ref_payload = decode_token(refresh_token, expected_type="refresh")
    assert ref_payload["sub"] == str(user_id)
    assert ref_payload["email"] == email
    assert ref_payload["type"] == "refresh"
    assert "jti" in ref_payload
    # Expiration is ~7 days
    ref_duration = ref_payload["exp"] - ref_payload["iat"]
    assert ref_duration == settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400


# ---------------------------------------------------------------------------
# 2. Signup Endpoint Tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_signup_success(client: AsyncClient):
    """POST /auth/signup creates account, returns access token, sets httpOnly refresh cookie."""
    payload = {
        "email": "user@example.com",
        "password": "ValidPassword123!",
    }
    response = await client.post("/auth/signup", json=payload)
    assert response.status_code == 201
    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["expires_in"] == 900
    assert data["user"]["email"] == "user@example.com"

    # Verify httpOnly refresh token cookie is set
    assert settings.COOKIE_NAME in response.cookies
    cookie = response.cookies[settings.COOKIE_NAME]
    decoded = decode_token(cookie, expected_type="refresh")
    assert decoded["email"] == "user@example.com"


@pytest.mark.asyncio
async def test_signup_short_password_rejected(client: AsyncClient):
    """Signup enforces minimum 8 characters password rule."""
    payload = {
        "email": "short@example.com",
        "password": "short",
    }
    response = await client.post("/auth/signup", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert data["code"] == "VALIDATION_ERROR"
    assert "details" in data


@pytest.mark.asyncio
async def test_signup_duplicate_email_rejected(client: AsyncClient):
    """Signup rejects duplicate email."""
    payload = {
        "email": "duplicate@example.com",
        "password": "ValidPassword123!",
    }
    res1 = await client.post("/auth/signup", json=payload)
    assert res1.status_code == 201

    res2 = await client.post("/auth/signup", json=payload)
    assert res2.status_code == 400
    data = res2.json()
    assert data["code"] == "USER_ALREADY_EXISTS"


# ---------------------------------------------------------------------------
# 3. Login Endpoint Tests & Lockout Logic (5 failures in 10 min -> 15 min lock)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    """POST /auth/login with valid credentials returns session and sets cookie."""
    # First sign up
    await client.post(
        "/auth/signup",
        json={"email": "loginuser@example.com", "password": "Password123!"},
    )

    # Login
    response = await client.post(
        "/auth/login",
        json={"email": "loginuser@example.com", "password": "Password123!"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == "loginuser@example.com"
    assert settings.COOKIE_NAME in response.cookies


@pytest.mark.asyncio
async def test_login_invalid_password(client: AsyncClient):
    """Failed login returns 401 and tracks remaining attempts."""
    await client.post(
        "/auth/signup",
        json={"email": "attempt@example.com", "password": "Password123!"},
    )

    response = await client.post(
        "/auth/login",
        json={"email": "attempt@example.com", "password": "WrongPassword!"},
    )
    assert response.status_code == 401
    data = response.json()
    assert data["code"] == "INVALID_CREDENTIALS"
    assert data["details"]["attempts_remaining"] == 4


@pytest.mark.asyncio
async def test_account_lockout_after_5_failed_logins(
    client: AsyncClient, test_db: InMemoryAsyncSession
):
    """5 failures in 10 minutes triggers 15-minute account lockout."""
    email = "lockout@example.com"
    await client.post(
        "/auth/signup",
        json={"email": email, "password": "Password123!"},
    )

    # 4 consecutive failures
    for attempt in range(1, 5):
        res = await client.post(
            "/auth/login",
            json={"email": email, "password": "BadPassword!"},
        )
        assert res.status_code == 401
        assert res.json()["details"]["attempts_remaining"] == 5 - attempt

    # 5th failure: triggers lockout (HTTP 423 Locked)
    res_5 = await client.post(
        "/auth/login",
        json={"email": email, "password": "BadPassword!"},
    )
    assert res_5.status_code == 423
    data_5 = res_5.json()
    assert data_5["code"] == "ACCOUNT_LOCKED"
    assert data_5["details"]["minutes_remaining"] == 15

    # 6th attempt (even with CORRECT password) is locked out!
    res_locked = await client.post(
        "/auth/login",
        json={"email": email, "password": "Password123!"},
    )
    assert res_locked.status_code == 423
    assert res_locked.json()["code"] == "ACCOUNT_LOCKED"


@pytest.mark.asyncio
async def test_lockout_expires_resets_account(client: AsyncClient, test_db: InMemoryAsyncSession):
    """Once locked_until timestamp passes, account automatically unlocks on next login."""
    email = "expiredlock@example.com"
    await client.post(
        "/auth/signup",
        json={"email": email, "password": "Password123!"},
    )

    # Manually simulate expired lock in the DB
    user = test_db.users_by_email[email]
    user.locked_until = datetime.now(UTC) - timedelta(minutes=1)
    user.failed_logins = 5

    # Login with correct password succeeds and clears lock
    res = await client.post(
        "/auth/login",
        json={"email": email, "password": "Password123!"},
    )
    assert res.status_code == 200
    assert user.locked_until is None
    assert user.failed_logins == 0


# ---------------------------------------------------------------------------
# 4. Refresh & Logout Endpoint Tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_refresh_token_rotation(client: AsyncClient):
    """POST /auth/refresh rotates the refresh token and issues a new access token."""
    signup_res = await client.post(
        "/auth/signup",
        json={"email": "refresher@example.com", "password": "Password123!"},
    )
    old_cookie = signup_res.cookies[settings.COOKIE_NAME]

    # Call refresh endpoint with existing cookie
    client.cookies.set(settings.COOKIE_NAME, old_cookie)
    refresh_res = await client.post("/auth/refresh")
    assert refresh_res.status_code == 200
    data = refresh_res.json()
    assert "access_token" in data
    assert data["user"]["email"] == "refresher@example.com"

    # Ensure new cookie was issued (rotated)
    new_cookie = refresh_res.cookies.get(settings.COOKIE_NAME)
    assert new_cookie is not None
    # JTI or signatures should differ
    old_payload = decode_token(old_cookie, expected_type="refresh")
    new_payload = decode_token(new_cookie, expected_type="refresh")
    assert old_payload["jti"] != new_payload["jti"]


@pytest.mark.asyncio
async def test_refresh_token_missing_rejected(client: AsyncClient):
    """POST /auth/refresh without cookie returns 401 REFRESH_TOKEN_MISSING."""
    client.cookies.clear()
    res = await client.post("/auth/refresh")
    assert res.status_code == 401
    assert res.json()["code"] == "REFRESH_TOKEN_MISSING"


@pytest.mark.asyncio
async def test_logout_clears_cookie(client: AsyncClient):
    """POST /auth/logout clears the refresh cookie."""
    signup_res = await client.post(
        "/auth/signup",
        json={"email": "logout@example.com", "password": "Password123!"},
    )
    client.cookies.set(settings.COOKIE_NAME, signup_res.cookies[settings.COOKIE_NAME])

    res = await client.post("/auth/logout")
    assert res.status_code == 200
    assert res.json()["message"] == "Logged out successfully"
    # Cookie should be deleted/cleared
    cookie_val = res.cookies.get(settings.COOKIE_NAME)
    assert cookie_val is None or cookie_val == '""' or cookie_val == ""


# ---------------------------------------------------------------------------
# 5. Protected Endpoint Tests (GET /auth/me)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_me_authenticated(client: AsyncClient):
    """GET /auth/me with valid Bearer token returns current user."""
    res = await client.post(
        "/auth/signup",
        json={"email": "me_user@example.com", "password": "Password123!"},
    )
    token = res.json()["access_token"]

    me_res = await client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert me_res.status_code == 200
    assert me_res.json()["email"] == "me_user@example.com"


@pytest.mark.asyncio
async def test_get_me_unauthorized(client: AsyncClient):
    """GET /auth/me without token returns 401 UNAUTHORIZED."""
    res = await client.get("/auth/me")
    assert res.status_code == 401
    assert res.json()["code"] == "UNAUTHORIZED"
