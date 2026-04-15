from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str
    x_secret_key: str
    qdrant_api_key: str
    qdrant_api_url: str
    qdrant_collection_name: str = "courses_coursenova"
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
