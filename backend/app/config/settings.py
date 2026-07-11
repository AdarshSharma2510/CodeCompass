from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "Repository Intelligence Copilot"
    APP_VERSION: str = "1.0.0"
    CHROMA_DB_PATH: str = "data/chroma"
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

settings = Settings()