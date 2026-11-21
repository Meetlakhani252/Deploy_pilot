"""Application configuration settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "DeployPilot"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = (
        "postgresql+asyncpg://deploypilot:deploypilot_secret@localhost:5432/deploypilot"
    )
    SECRET_KEY: str = "deploypilot_super_secret_jwt_key_change_in_production"
    FERNET_KEY: str = "u_vI33_hS-96B1QYh1kYwQf4L0cZ3N-7g6Lp5N-yq8M="
    ENVIRONMENT: str = "development"

    # JWT & Session settings
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15  # Short-lived access token (15 min)
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7  # Rotating refresh token (7 days)
    COOKIE_NAME: str = "deploypilot_refresh_token"
    COOKIE_SECURE: bool = False  # Set to True in HTTPS/production
    COOKIE_SAMESITE: str = "lax"

    # Account Lockout settings (FR-01, M1: 5 failures in 10 min -> 15 min lock)
    LOCKOUT_THRESHOLD: int = 5
    LOCKOUT_WINDOW_MINUTES: int = 10
    LOCKOUT_DURATION_MINUTES: int = 15

    # CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
