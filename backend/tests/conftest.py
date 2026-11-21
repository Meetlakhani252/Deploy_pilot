"""Test database and fixtures for DeployPilot Authentication."""

import uuid
from datetime import UTC, datetime
from typing import Any

import pytest
from httpx import ASGITransport, AsyncClient

from app.core.config import settings
from app.core.database import get_db
from app.main import app
from app.models.models import AuditLog, Setting, User

settings.ENVIRONMENT = "test"


class InMemoryAsyncSession:
    """Lightweight in-memory AsyncSession implementation for unit & API testing."""

    def __init__(self) -> None:
        self.users: dict[uuid.UUID, User] = {}
        self.users_by_email: dict[str, User] = {}
        self.audit_logs: list[AuditLog] = []
        self.settings: dict[uuid.UUID, Setting] = {}

    def add(self, obj: Any) -> None:
        if isinstance(obj, User):
            self.users[obj.id] = obj
            self.users_by_email[obj.email.strip().lower()] = obj
        elif isinstance(obj, AuditLog):
            if not getattr(obj, "id", None):
                obj.id = uuid.uuid4()
            if not getattr(obj, "ts", None):
                obj.ts = datetime.now(UTC)
            self.audit_logs.append(obj)
        elif isinstance(obj, Setting):
            self.settings[obj.user_id] = obj

    async def commit(self) -> None:
        pass

    async def refresh(self, obj: Any) -> None:
        pass

    async def close(self) -> None:
        pass

    async def execute(self, stmt: Any) -> Any:
        compiled = stmt.compile()
        sql_str = str(compiled)
        params = compiled.params

        class ResultWrapper:
            def __init__(self, item: Any) -> None:
                self._item = item

            def scalar_one_or_none(self) -> Any:
                return self._item

            def scalar(self) -> Any:
                return self._item

            def scalars(self) -> Any:
                class ScalarsWrapper:
                    def __init__(self, items: list[Any]) -> None:
                        self._items = items

                    def all(self) -> list[Any]:
                        return self._items

                    def first(self) -> Any:
                        return self._items[0] if self._items else None

                return ScalarsWrapper([self._item] if self._item is not None else [])

        # 1. Query count of AuditLog
        if "count" in sql_str.lower() and "audit_logs" in sql_str.lower():
            user_id = None
            window_start = None
            for k, v in params.items():
                if isinstance(v, uuid.UUID) or (isinstance(v, str) and len(v) == 36 and "-" in v):
                    try:
                        user_id = uuid.UUID(str(v))
                    except ValueError:
                        pass
                elif isinstance(v, datetime):
                    window_start = v

            count = 0
            for log in self.audit_logs:
                if user_id and log.user_id != user_id:
                    continue
                if log.event_type != "auth.login_failed":
                    continue
                if window_start and log.ts < window_start:
                    continue
                count += 1
            return ResultWrapper(count)

        # 2. Query User
        if "users" in sql_str.lower():
            # Check by email
            email_param = None
            id_param = None
            for k, v in params.items():
                if "email" in k or (isinstance(v, str) and "@" in v):
                    email_param = str(v).strip().lower()
                elif "id" in k or isinstance(v, uuid.UUID):
                    try:
                        id_param = uuid.UUID(str(v))
                    except (ValueError, TypeError):
                        pass

            if email_param:
                user = self.users_by_email.get(email_param)
                return ResultWrapper(user)
            if id_param:
                user = self.users.get(id_param)
                return ResultWrapper(user)

        return ResultWrapper(None)


@pytest.fixture
def test_db() -> InMemoryAsyncSession:
    """Fixture providing a clean in-memory database session for each test."""
    return InMemoryAsyncSession()


@pytest.fixture
async def client(test_db: InMemoryAsyncSession):
    """HTTP client wired to the in-memory database."""

    async def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
