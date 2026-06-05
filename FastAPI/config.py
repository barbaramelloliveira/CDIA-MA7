from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # 👈 aqui está a correção

class Settings(BaseSettings):
    app_name: str = "Bella Tavola API"
    app_version: str = "1.0.0"
    debug: bool = False
    max_mesas: int = 20
    max_pessoas_por_mesa: int = 8

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore"
    )

settings = Settings()