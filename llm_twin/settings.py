from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # MongoDB database
    DATABASE_HOST: str = "mongodb://llm_twin:llm_twin@127.0.0.1:27017"
    DATABASE_NAME: str = "twin"


settings = Settings()
