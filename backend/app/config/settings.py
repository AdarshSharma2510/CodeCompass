from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BACKEND_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = BACKEND_DIR / ".env"


class Settings(BaseSettings):
    HF_ACCESS_TOKEN: str
    EMBEDDING_MODEL: str

    CHROMA_DB_PATH: Path = BACKEND_DIR / "data" / "chroma"
    REPOSITORY_PATH: Path = BACKEND_DIR / "data" / "repository"
    UPLOAD_PATH: Path = BACKEND_DIR / "data" / "upload.zip"

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()