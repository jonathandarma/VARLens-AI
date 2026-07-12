from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    api_cors_origins: str = "http://localhost:3000"
    database_url: str = "sqlite:///./varlens.db"
    upload_dir: str = "./data/uploads"
    yolo_model: str = ""
    openai_api_key: str = ""
    max_upload_mb: int = 512

    @property
    def upload_path(self) -> Path:
        path = Path(self.upload_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path

settings = Settings()
