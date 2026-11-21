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

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
