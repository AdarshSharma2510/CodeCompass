from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "CodeCompass"
    APP_VERSION: str = "1.0.0"

    CHROMA_DB_PATH: str = "data/chroma"

    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    HF_TOKEN: str | None = None
    
    model_config = SettingsConfigDict(
        env_file='.env',
        extra = 'ignore',
    )

settings = Settings()