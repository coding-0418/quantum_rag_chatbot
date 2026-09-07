from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    log_level: str = "INFO"

    postgres_host: str = "postgres"
    postgres_port: int = 5432
    postgres_db: str = "quantum_rag"
    postgres_user: str = "quantum_rag"
    postgres_password: str = "change_me"
    database_url: str = (
        "postgresql+asyncpg://quantum_rag:change_me@postgres:5432/quantum_rag"
    )

    neo4j_uri: str = "bolt://neo4j:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "change_me"

    redis_host: str = "redis"
    redis_port: int = 6379
    redis_db: int = 0

    faiss_index_path: str = "data/faiss_index/knowledge_base.index"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    quantum_backend: str = "aer_simulator"
    quantum_shots: int = 1024

    streamlit_api_base_url: str = "http://api:8000"


@lru_cache
def get_settings() -> Settings:
    return Settings()
