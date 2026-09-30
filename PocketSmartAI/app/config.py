from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    app_name: str = "PocketSmart AI"

    secret_key: str = "dev-secret-change-me"

    gemini_api_key: str | None = None

    gemini_model: str = "gemini-3.8-flash"

    database_url: str = "sqlite:///./data/pocketsmart.db"

    access_token_expire_minutes: int = 1440

    max_image_mb: int = 5

    frontend_origin: str = "http://127.0.0.1:8000"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()