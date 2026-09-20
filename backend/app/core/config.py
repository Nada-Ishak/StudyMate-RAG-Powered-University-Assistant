from pathlib import Path
from pydantic_settings import BaseSettings


PROJECT_DIR = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    app_name: str = "StudyMate API"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_device: str = "cuda"
    llm_model: str = "mistral"
    chroma_collection: str = "studymate_documents"

    vector_store_path: str = str(
        PROJECT_DIR / "backend" / "data" / "vector_store"
    )

    class Config:
        env_file = ".env"


settings = Settings()