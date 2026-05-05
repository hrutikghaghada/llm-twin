from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Gemini API
    GEMINI_MODEL_ID: str = "gemini-3.1-flash-lite-preview"
    GEMINI_API_KEY: str | None = None

    # Huggingface API
    HUGGINGFACE_ACCESS_TOKEN: str | None = None

    # MongoDB database
    DATABASE_HOST: str = "mongodb://llm_twin:llm_twin@127.0.0.1:27017"
    DATABASE_NAME: str = "twin"

    # Qdrant vector database
    USE_QDRANT_CLOUD: bool = False
    QDRANT_DATABASE_HOST: str = "localhost"
    QDRANT_DATABASE_PORT: int = 6333
    QDRANT_CLOUD_URL: str = "str"
    QDRANT_APIKEY: str | None = None

    # RAG
    TEXT_EMBEDDING_MODEL_ID: str = "sentence-transformers/all-MiniLM-L6-v2"
    RERANKING_CROSS_ENCODER_MODEL_ID: str = "cross-encoder/ms-marco-MiniLM-L-4-v2"
    RAG_MODEL_DEVICE: str = "cpu"

    @property
    def GEMINI_MAX_TOKEN_WINDOW(self) -> int:
        official_max_token_window = {
            "gemini-2.5-flash": 1048576,
            "gemini-3-flash-preview": 1048576,
            "gemini-3.1-flash-lite-preview": 1048576,
        }.get(self.GEMINI_MODEL_ID, 1048576)

        max_token_window = int(official_max_token_window * 0.80)

        return max_token_window


settings = Settings()
